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
