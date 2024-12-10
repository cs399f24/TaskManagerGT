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
