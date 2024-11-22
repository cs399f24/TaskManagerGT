import boto3
import sys
import json

# Initialize the boto3 client for API Gateway
client = boto3.client('apigateway', region_name='us-east-1')

# Check if TaskManagerAPI already exists
response = client.get_rest_apis()
apis = response.get('items', [])

for api in apis:
    if api.get('name') == 'TaskManagerAPI':
        print('API already exists')
        sys.exit(0)

# Create the Task Manager API
response = client.create_rest_api(
    name='TaskManagerAPI',
    description='API to manage tasks.',
    endpointConfiguration={
        'types': [
            'REGIONAL',
        ]
    }
)
api_id = response["id"]

# Get the root resource ID
resources = client.get_resources(restApiId=api_id)
root_id = [resource for resource in resources["items"] if resource["path"] == "/"][0]["id"]

# Create the 'tasks' resource
tasks = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='tasks'
)
tasks_resource_id = tasks["id"]

# Set up the GET method for retrieving tasks
tasks_method = client.put_method(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)

tasks_response = client.put_method_response(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={
        'application/json': 'Empty'
    }
)

# Get the ARN for the viewTaskFunction Lambda function
lambda_client = boto3.client('lambda', region_name='us-east-1')
lambda_arn = lambda_client.get_function(FunctionName='viewTaskFunction')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Get the ARN for the IAM LabRole
iam_client = boto3.client('iam')
lab_role = iam_client.get_role(RoleName='LabRole')['Role']['Arn']

# Set up the integration for the GET method to invoke the viewTaskFunction Lambda
tasks_integration = client.put_integration(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='GET',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=uri
)

# Create the 'create' resource for adding tasks
create_task = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='create'
)
create_task_resource_id = create_task["id"]

# Set up the POST method for creating a new task
create_task_method = client.put_method(
    restApiId=api_id,
    resourceId=create_task_resource_id,
    httpMethod='POST',
    authorizationType='NONE'
)

create_task_response = client.put_method_response(
    restApiId=api_id,
    resourceId=create_task_resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': False,
        'method.response.header.Access-Control-Allow-Origin': False,
        'method.response.header.Access-Control-Allow-Methods': False
    },
    responseModels={
        'application/json': 'Empty'
    }
)

# Get the ARN for the addTaskFunction Lambda function
lambda_arn = lambda_client.get_function(FunctionName='addTaskFunction')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Set up the integration for the POST method to invoke the addTaskFunction Lambda
create_task_integration = client.put_integration(
    restApiId=api_id,
    resourceId=create_task_resource_id,
    httpMethod='POST',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=uri
)

# Create the 'delete' resource for deleting tasks
delete_task = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='delete'
)
delete_task_resource_id = delete_task["id"]

# Set up the DELETE method for deleting tasks
delete_task_method = client.put_method(
    restApiId=api_id,
    resourceId=delete_task_resource_id,
    httpMethod='DELETE',
    authorizationType='NONE'
)

delete_task_response = client.put_method_response(
    restApiId=api_id,
    resourceId=delete_task_resource_id,
    httpMethod='DELETE',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': False,
        'method.response.header.Access-Control-Allow-Origin': False,
        'method.response.header.Access-Control-Allow-Methods': False
    },
    responseModels={
        'application/json': 'Empty'
    }
)

# Get the ARN for the deleteTaskFunction Lambda function
lambda_arn = lambda_client.get_function(FunctionName='deleteTaskFunction')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Set up the integration for the DELETE method to invoke the deleteTaskFunction Lambda
delete_task_integration = client.put_integration(
    restApiId=api_id,
    resourceId=delete_task_resource_id,
    httpMethod='DELETE',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=uri
)

# Set up the OPTIONS method for CORS
for method in ['GET', 'POST', 'DELETE']:
    resource_id = None
    if method == 'GET':
        resource_id = tasks_resource_id
    elif method == 'POST':
        resource_id = create_task_resource_id
    elif method == 'DELETE':
        resource_id = delete_task_resource_id

    # Set up the OPTIONS method for CORS support
    client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
    )

    client.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': False,
            'method.response.header.Access-Control-Allow-Origin': False,
            'method.response.header.Access-Control-Allow-Methods': False
        },
        responseModels={
            'application/json': 'Empty'
        }
    )

    client.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        type='MOCK',
        requestTemplates={
            'application/json': '{"statusCode": 200}'
        }
    )

    client.put_integration_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
            'method.response.header.Access-Control-Allow-Methods': '\'POST\',\'OPTIONS\',\'DELETE\',\'GET\'',
            'method.response.header.Access-Control-Allow-Origin': '\'*\''
        }
    )

print("DONE")
