import boto3

# Initialize the Cognito client
cognito_client = boto3.client('cognito-idp', region_name='your-region')

# Create a user pool
response = cognito_client.create_user_pool(
    PoolName='your_pool_name',  # Replace with your desired pool name
    Policies={
        'PasswordPolicy': {
            'MinimumLength': 8,
            'RequireUppercase': True,
            'RequireLowercase': True,
            'RequireNumbers': True,
            'RequireSymbols': True,
            'TemporaryPasswordValidityDays': 7
        }
    },
    AutoVerifiedAttributes=['email'],  # Replace or add attributes to auto-verify as needed
    AliasAttributes=[],  # Specify alias attributes if required
    UsernameAttributes=[],  # Specify username attributes if required
    UsernameConfiguration={
        'CaseSensitive': True
    },
    AccountRecoverySetting={
        'RecoveryMechanisms': [
            {'Priority': 1, 'Name': 'verified_email'}  # Replace or add recovery mechanisms
        ]
    }
)

user_pool_id = response['UserPool']['Id']
print(f"Created User Pool with ID: {user_pool_id}")

# Create an app client
app_client_response = cognito_client.create_user_pool_client(
    UserPoolId=user_pool_id,
    ClientName='your_app_client_name',  # Replace with your app client name
    GenerateSecret=False,  # Set to True if using a private client
    AllowedOAuthFlows=['implicit'],  # Replace with desired OAuth flows
    AllowedOAuthScopes=['email', 'openid'],  # Replace with desired scopes
    AllowedOAuthFlowsUserPoolClient=True,
    CallbackURLs=['https://your-app-callback-url'],  # Replace with your callback URL(s)
    ExplicitAuthFlows=[
        'ALLOW_REFRESH_TOKEN_AUTH',
        'ALLOW_CUSTOM_AUTH',
        'ALLOW_USER_SRP_AUTH',
        'ALLOW_USER_PASSWORD_AUTH'
    ]
)

app_client_id = app_client_response['UserPoolClient']['ClientId']
print(f"Created App Client with ID: {app_client_id}")

# Configure a domain for the hosted UI
cognito_client.create_user_pool_domain(
    Domain='your-unique-domain-name',  # Replace with your domain name
    UserPoolId=user_pool_id
)
print("Hosted UI domain configured")

# Create a resource server
resource_server_response = cognito_client.create_resource_server(
    UserPoolId=user_pool_id,
    Identifier='your-resource-server-identifier',  # Replace with your resource server identifier
    Name='your_resource_server_name',  # Replace with your resource server name
    Scopes=[
        {'ScopeName': 'your_scope_name', 'ScopeDescription': "Description of your scope."}  # Replace with desired scope details
    ]
)

print("Resource server created")

# Replace the hosted UI URL components with your details
hosted_ui_url = "https://your-domain.auth.your-region.amazoncognito.com/login?client_id=your_client_id&response_type=code&scope=email+openid+phone&redirect_uri=https://your-redirect-uri"
print(f"Hosted UI URL: {hosted_ui_url}")

