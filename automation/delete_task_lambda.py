import json
import boto3
from botocore.exceptions import ClientError

# Initialize the DynamoDB resource and table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')  # Replace with your DynamoDB table name

def lambda_handler(event, context):
    """
    Lambda function to delete a task from DynamoDB.
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

        # Delete the task from DynamoDB
        response = table.delete_item(
            Key={
                'userId': user_id,
                'taskName': task_name
            }
        )

        if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Task deleted successfully'})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Task not found'})
            }

    except ClientError as e:
        # Handle any errors that occur during the DynamoDB operation
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Error deleting task: {str(e)}"})
        }
    except Exception as e:
        # Handle general exceptions
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Error: {str(e)}"})
        }
