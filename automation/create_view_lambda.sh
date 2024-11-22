#!/bin/bash

# Define Lambda function name
LAMBDA_FUNCTION_NAME="getUserTasks"

# Check if the function already exists
if aws lambda get-function --function-name $LAMBDA_FUNCTION_NAME >/dev/null 2>&1; then
    echo "Function '$LAMBDA_FUNCTION_NAME' already exists"
    exit 1
fi

# Define the IAM role that Lambda will use (Make sure the role exists with required permissions)
ROLE="arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role"  # Replace with your actual role ARN

# Lambda function source file
LAMBDA_FILE="get_user_tasks_lambda.py"

# Lambda zip file name
ZIP_FILE="get_user_tasks_lambda.zip"

# Zip the Lambda function code
zip $ZIP_FILE $LAMBDA_FILE

# Create the Lambda function
aws lambda create-function \
    --function-name $LAMBDA_FUNCTION_NAME \
    --runtime python3.9 \
    --role $ROLE \
    --zip-file fileb://$ZIP_FILE \
    --handler get_user_tasks_lambda.lambda_handler \
    --timeout 30 \
    --memory-size 128

# Wait for the function to be created and active
aws lambda wait function-active --function-name $LAMBDA_FUNCTION_NAME

# Publish a version of the Lambda function
aws lambda publish-version --function-name $LAMBDA_FUNCTION_NAME

echo "Lambda function '$LAMBDA_FUNCTION_NAME' has been successfully created and versioned."
