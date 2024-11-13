
# Lambda
- Open Lambda and click Create Function
- Use Author from scratch
- Name your function so that you know it is for Cognito Token Authentication
- Select the Runtime as python 3.xx and leave Architechture as x86_64
- Under Change default execution role click Use an existing role and Choose LabRole
- Below is the python code that will go into your lambda function for verifying your Cognito Authentication Token but you need to update it with all your information
```python
import json
import urllib.parse
import urllib.request

def lambda_handler(event, context):
    try:
        # Log the incoming event for debugging
        print("Received event:", json.dumps(event))

        # Get the authorization code from the query parameters
        auth_code = event['queryStringParameters'].get('code')
        if not auth_code:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Authorization code missing'}),
                'headers': {'Content-Type': 'application/json'}
            }

        # Cognito token URL
        token_url = "(Insert Your Cognito Token URl in the quotes)"

        # Set the client details
        client_id = "(Insert Cognito Client Id in quotes)" 

        # Set the payload for the token request
        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': '(Insert your API Gateway Callback URL in the quotes)',
            'client_id': client_id
        }

        # Encode the payload
        data = urllib.parse.urlencode(payload).encode()

        # Create the request
        req = urllib.request.Request(token_url, data=data, method='POST')

        # Add headers for the request
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')

        # Make the request and get the response
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode()
            tokens = json.loads(response_data)

        # Log the response (for debugging)
        print("Tokens received:", tokens)

        # Redirect to the frontend page (Task Manager) and pass tokens as query parameters
        return {
            'statusCode': 302,
            'headers': {
                'Location': f'(Enter Your original S3 Bucket index link but keep query after)?access_token={tokens["access_token"]}&id_token={tokens["id_token"]}&refresh_token={tokens["refresh_token"]}'  # Redirect with tokens
            }
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
```