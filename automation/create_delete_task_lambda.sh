#!/bin/bash

# Set the path to the Python script in the automation folder
LAMBDA_PYTHON_FILE="./automation/delete_task_lambda.py"

# Check if delete_task_lambda.py exists in the automation directory
if [ ! -f "$LAMBDA_PYTHON_FILE" ]; then
    echo "Error: delete_task_lambda.py not found in automation directory!"
    exit 1
fi

# Make sure the function does not already exist
if aws lambda get-function --function-name DeleteTask >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

# Get the IAM role ARN (ensure the role exists)
ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)

# Zip the delete_task_lambda.py script
zip delete_task_lambda.zip "$LAMBDA_PYTHON_FILE"

# Create the Delete Task Lambda function
aws lambda create-function --function-name DeleteTask \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://delete_task_lambda.zip \
  --handler delete_task_lambda.lambda_handler

# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name DeleteTask  

# Publish a version of the function
aws lambda publish-version --function-name DeleteTask

echo "DeleteTask Lambda function created and version published."

