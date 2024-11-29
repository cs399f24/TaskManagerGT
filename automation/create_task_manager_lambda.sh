#!/bin/bash

# Set the path to the Python script for the Lambda function
LAMBDA_PYTHON_FILE="./automation/taskManagerLambda.py"

# Check if the Python file exists
if [ ! -f "$LAMBDA_PYTHON_FILE" ]; then
    echo "Error: taskManagerLambda.py not found!"
    exit 1
fi

# Create IAM Role (if not already created)
ROLE_NAME="LambdaExecutionRole"
ROLE_POLICY="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"

# Check if the IAM Role exists
if ! aws iam get-role --role-name $ROLE_NAME >/dev/null 2>&1; then
    echo "Creating IAM Role..."
    aws iam create-role --role-name $ROLE_NAME --assume-role-policy-document file://trust-policy.json
    aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn $ROLE_POLICY
else
    echo "IAM Role $ROLE_NAME already exists."
fi

# Zip the Lambda function Python script
zip task_manager_lambda.zip "$LAMBDA_PYTHON_FILE"

# Get the IAM Role ARN
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query "Role.Arn" --output text)

# Create the Lambda function
aws lambda create-function --function-name taskManagerLambda \
  --runtime python3.9 \
  --role $ROLE_ARN \
  --zip-file fileb://task_manager_lambda.zip \
  --handler taskManagerLambda.lambda_handler

echo "Lambda function taskManagerLambda created successfully."
