import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    user_id = event.get('user_id')  # User ID passed in the event
    
    if not user_id:
        return {
            'statusCode': 400,
            'body': json.dumps('User ID is required')
        }
    
    # Query DynamoDB for tasks associated with the user
    try:
        response = dynamodb.query(
            TableName='Tasks',
            KeyConditionExpression='UserId = :user_id',
            ExpressionAttributeValues={
                ':user_id': {'S': user_id}
            }
        )
        
        tasks = response.get('Items', [])
        
        # Prepare the response format
        task_list = []
        for task in tasks:
            task_list.append({
                'TaskId': task['TaskId']['S'],
                'TaskName': task['TaskName']['S'],
                'Status': task['Status']['S'],
                'DueDate': task['DueDate']['S'],
                'Priority': task.get('Priority', {}).get('S', 'Not set')
            })
        
        return {
            'statusCode': 200,
            'body': json.dumps({'tasks': task_list})
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving tasks: {e.response['Error']['Message']}")
        }
