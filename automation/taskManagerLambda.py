import json

def lambda_handler(event, context):
    """
    Lambda function to handle tasks for Task Manager API.
    It processes incoming events from the API Gateway and returns a response.
    """
    # Example: Processing a POST request to add a task
    if event['httpMethod'] == 'POST':
        # Get task details from the body
        body = json.loads(event['body'])
        task_name = body.get('task_name', 'Untitled Task')
        task_description = body.get('task_description', 'No description')

        # Simulate adding the task (you can integrate with a database here)
        task = {
            'task_id': 1,  # In real-world use, generate or fetch from DB
            'task_name': task_name,
            'task_description': task_description
        }

        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Task created successfully',
                'task': task
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # CORS header
            }
        }
        
        return response

    # Default for unsupported methods or other handling
    return {
        'statusCode': 400,
        'body': json.dumps({'message': 'Method not supported'})
    }
