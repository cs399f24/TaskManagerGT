
# Task Manager GT

<img width="791" alt="Screenshot 2024-12-10 at 1 25 57 PM" src="https://github.com/user-attachments/assets/faed544c-42cc-40cb-a20f-74aaf1115709">

# Project Description
A Task Manager website that offers a seamless experience for users to sign up or log in securely. Each user has access to their own private task list, ensuring personalized task management. The website allows you to effortlessly create an unlimited number of tasks and delete them as needed, making it a simple and efficient tool to stay organized.

# Steps:

Clone the repository

Go to the aws console, and open the s3 page

Create the s3 bucket

Uncheck Block Public Access settings for this bucket and acknowledgement box

Change bucket policy - the bucket policy in our texts

Upload the index.html and the task-manager.html files from the templates folder without links in s3

Open the aws amplify page

Create new app

Deploy without git 

click next

Choose s3

Browse

Choose s3 bucket

S3 links should now be in https for index.html and task-manager.html

Create Dynamodb with with partition key: user_id (String) and sort key: task_id (String) and default settings

API gateway

Create a rest API and build with whatever name

Click create resource and name it task and don't enable cors

Select tasks and hit create resource and name the resource {taskId}

Go to lambda

Click Create function

Author from scratch

Name first function GetTask

Change Runtime to python 3.*

Click change default execution role

Use the existing role LabRole

copy and paste the following code under source code then hit deploy:
```
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TasksTable')

def lambda_handler(event, context):
    # Extract the user ID from the Cognito JWT token (from API Gateway context)
    user_id = event['requestContext']['authorizer']['claims']['sub']
    
    # Query DynamoDB to get the tasks for this user
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    
    tasks = response.get('Items', [])
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Allow all origins or specify your domain
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',  # Allowed methods
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',  # Allowed headers
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'tasks': tasks})
    }
```

Do the same and name it DeleteTask:

```
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TasksTable')

def lambda_handler(event, context):
    # Extract user ID from the token
    user_id = event['requestContext']['authorizer']['claims']['sub']
    
    # Get task_id from the URL path
    task_id = event['pathParameters']['taskId']
    
    # Delete the task from DynamoDB
    table.delete_item(
        Key={
            'user_id': user_id,
            'task_id': task_id
        }
    )
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Allow all origins or specify your domain
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',  # Allowed methods
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',  # Allowed headers
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': 'Task deleted successfully'})
    }
```

Do the same and name it CreateTask:

```
import json
import boto3
from uuid import uuid4
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TasksTable')

def lambda_handler(event, context):
    try:
        # Log the entire event for debugging purposes
        print("Received event: ", json.dumps(event))  # This will help you inspect the event object
        
        # Log Authorization header to see if the token is being passed correctly
        authorization_header = event['headers'].get('Authorization', 'No Authorization Header')
        print("Authorization Header: ", authorization_header)

        # Extract user ID from the token
        if 'requestContext' in event and 'authorizer' in event['requestContext']:
            user_id = event['requestContext']['authorizer']['claims']['sub']
        else:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Unauthorized', 'error': 'No authorizer found in the request'})
            }

        # Get task details from the request body
        body = json.loads(event['body'])
        task_name = body.get('task_name')

        if not task_name:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'task_name is required'})
            }

        # Generate a new task ID and current timestamp
        task_id = str(uuid4())
        created_at = datetime.utcnow().isoformat()

        # Insert new task into DynamoDB
        table.put_item(
            Item={
                'user_id': user_id,
                'task_id': task_id,
                'task_name': task_name,
                'created_at': created_at
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins or specify your domain
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',  # Allowed methods
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',  # Allowed headers
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Task created successfully', 'task_id': task_id})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins or specify your domain
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',  # Allowed methods
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',  # Allowed headers
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Failed to create task', 'error': str(e)})
        }
```

Go back to API gateway and attach functions

Click create methods on tasks

Get is GetFunction

Check lambda proxy integration

Open HTTP request headers

Name is Authorizer and make sure required is selected

Click /tasks and hit enable cors

Enable everything except what is under additional settings

Do the same for /{taskId}

Open cognito 

Create user pool

Select SPA

Configure options are email and username

Set return url to task-manager.html from s3 the https link

Go to app clients

Go to domain under branding and select actions and select edit cognito domain branding version

Switch to Hosted UI (classic)

Copy your Cognito domain that is under cognito domain and save it somewhere

Open view login page

Copy login page link

Navigate back to API Gateway

Select your Api

Select authorizers

Create authorizer

Name it CongitoUserAuth

Choose Cognito under Authorizer type

Choose your created cognito user pool

As the token source make it Authorization

Go back to resources

Click on your Get method

Scroll down to method requests and click edit

Select your Cognito authorizer and hit save

Redo the same for the POST and DELETE methods

Hit Deloy API

Click new stage and name your API Stage

Under Stages you should have an invoke url

Save this somewhere

Open index.html in an Cloud9

Add your AWS Cognito Hosted Login URL under where it says link to AWS Cognito login in the quotes

Save change

Put updated index into S3 bucket

Open task-manager.html in IDE

On Line 100 insert the same link you had put into the index.html

On Line 106 add that link again but delete everything after amazoncognito.com/ and add oauth2/token instead

On line 109 your redirect_uri is your object url for your task manager

On line 110 add your client id from your Cognito app client

On line 133 for your cognito hosted ui url add the same on that you did in the index.html

On line 139 add your API gateway invoke url from stages

On line 162 you are going to add your invoke url and leave the /${task.task_id}

On line 202 add your invoke url again

On line 230 add your link from your index object url

Save all those changes

Upload task-manager.html into your s3 bucket

To access task manager open your s3 index object link in your browser

