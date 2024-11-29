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
        token_url = "https://authent.auth.us-east-1.amazoncognito.com/oauth2/token"

        # Set the client details
        client_id = "4kommh5cddnogjvcru85m237c6" 

        # Set the payload for the token request
        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': 'https://gqtens6p9b.execute-api.us-east-1.amazonaws.com/deploy1/callback',
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
                'Location': f'http://taskmanagergt.s3-website-us-east-1.amazonaws.com/task-manager.html?access_token={tokens["access_token"]}&id_token={tokens["id_token"]}&refresh_token={tokens["refresh_token"]}'  # Redirect with tokens
            }
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
