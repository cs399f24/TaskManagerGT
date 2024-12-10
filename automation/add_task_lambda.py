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
