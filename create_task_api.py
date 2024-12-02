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

# Create resources for tasks, create, delete, and auth
tasks = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='tasks'
)
tasks_resource_id = tasks["id"]

create_task = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='create'
)
create_task_resource_id = create_task["id"]

delete_task = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='delete'
)
delete_task_resource_id = delete_task["id"]

auth = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='auth'
)
auth_resource_id = auth["id"]

# Lambda client
lambda_client = boto3.client('lambda', region_name='us-east-1')

# IAM client for LabRole ARN
iam_client = boto3.client('iam')
lab_role = iam_client.get_role(RoleName='LabRole')['Role']['Arn']

# ----- Set up integrations for tasks -----
view_task_lambda_arn = lambda_client.get_function(FunctionName='viewTaskFunction')['Configuration']['FunctionArn']
view_task_uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{view_task_lambda_arn}/invocations'

client.put_method(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)

client.put_integration(
    restApiId=api_id,
    resourceId=tasks_resource_id,
    httpMethod='GET',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=view_task_uri
)

# ----- Set up integration for creating tasks -----
add_task_lambda_arn = lambda_client.get_function(FunctionName='addTaskFunction')['Configuration']['FunctionArn']
add_task_uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{add_task_lambda_arn}/invocations'

client.put_method(
    restApiId=api_id,
    resourceId=create_task_resource_id,
    httpMethod='POST',
    authorizationType='NONE'
)

client.put_integration(
    restApiId=api_id,
    resourceId=create_task_resource_id,
    httpMethod='POST',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=add_task_uri
)

# ----- Set up integration for deleting tasks -----
delete_task_lambda_arn = lambda_client.get_function(FunctionName='deleteTaskFunction')['Configuration']['FunctionArn']
delete_task_uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{delete_task_lambda_arn}/invocations'

client.put_method(
    restApiId=api_id,
    resourceId=delete_task_resource_id,
    httpMethod='DELETE',
    authorizationType='NONE'
)

client.put_integration(
    restApiId=api_id,
    resourceId=delete_task_resource_id,
    httpMethod='DELETE',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=delete_task_uri
)

# ----- Set up integration for auth -----
auth_function_arn = lambda_client.get_function(FunctionName='authFunction')['Configuration']['FunctionArn']
auth_uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{auth_function_arn}/invocations'

client.put_method(
    restApiId=api_id,
    resourceId=auth_resource_id,
    httpMethod='POST',
    authorizationType='NONE'
)

client.put_integration(
    restApiId=api_id,
    resourceId=auth_resource_id,
    httpMethod='POST',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=auth_uri
)

# ----- Set up OPTIONS methods for CORS -----
resources = {
    'GET': tasks_resource_id,
    'POST': create_task_resource_id,
    'DELETE': delete_task_resource_id,
    'AUTH': auth_resource_id
}

for method, resource_id in resources.items():
    client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
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
