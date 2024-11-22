import boto3

# Initialize the Cognito client
cognito_client = boto3.client('cognito-idp', region_name='us-east-1')

# Create a user pool
response = cognito_client.create_user_pool(
    PoolName='PoolofUsers',
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
    AutoVerifiedAttributes=['email'],  # Email is auto-verified
    AliasAttributes=[],  # No aliases enabled
    UsernameAttributes=[],  # Username-based authentication
    UsernameConfiguration={
        'CaseSensitive': True
    },
    AccountRecoverySetting={
        'RecoveryMechanisms': [
            {'Priority': 1, 'Name': 'verified_email'}  # Recovery via email
        ]
    }
)

user_pool_id = response['UserPool']['Id']
print(f"Created User Pool with ID: {user_pool_id}")


# Create an app client
app_client_response = cognito_client.create_user_pool_client(
    UserPoolId=user_pool_id,
    ClientName='app_client',
    GenerateSecret=False,  # Public client
    AllowedOAuthFlows=['implicit'],  # Enable implicit grant
    AllowedOAuthScopes=['email', 'openid'],  # Scopes
    AllowedOAuthFlowsUserPoolClient=True,
    CallbackURLs=['http://taskmanagergt.s3-website-us-east-1.amazonaws.com/task-manager.html'],
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
    Domain='authent',
    UserPoolId=user_pool_id
)
print("Hosted UI domain configured")


# Create a resource server
resource_server_response = cognito_client.create_resource_server(
    UserPoolId=user_pool_id,
    Identifier='https://gqtens6p9b.execute-api.us-east-1.amazonaws.com/dev/callback',
    Name='task_manager_api',
    Scopes=[
        {'ScopeName': 'task_management', 'ScopeDescription': "Permission to access task management functionality."}
    ]
)

print("Resource server created")


hosted_ui_url = "https://authent.auth.us-east-1.amazoncognito.com/login?client_id=4kommh5cddnogjvcru85m237c6&response_type=code&scope=email+openid+phone&redirect_uri=http://taskmanagergt.s3-website-us-east-1.amazonaws.com/index.html"
print(f"Hosted UI URL: {hosted_ui_url}")

