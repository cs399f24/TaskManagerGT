import json
import boto3
from botocore.exceptions import ClientError

# Initialize the DynamoDB resource and table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')  # Replace with your DynamoDB table name

def lambda_handler(event, context):
    """
    Lambda function to add a new task to DynamoDB.
    """
    try:
        # Parse the incoming event (assuming it's passed as JSON in the event body)
        body = json.loads(event['body'])
        user_id = body['userId']
        task_name = body['taskName']

        # Check if userId and taskName are provided
        if not user_id or not task_name:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'userId and taskName are required'})
            }

        # Add the task to DynamoDB
        response = table.put_item(
            Item={
                'userId': user_id,
                'taskName': task_name
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Task added successfully', 'task': body})
        }

    except ClientError as e:
        # Handle any errors that occur during the DynamoDB operation
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Error adding task: {str(e)}"})
        }
    except Exception as e:
        # Handle general exceptions
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Error: {str(e)}"})
        }
