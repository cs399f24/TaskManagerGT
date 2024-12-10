#!/bin/bash

# Set the path to the Python script in the automation folder
LAMBDA_PYTHON_FILE="./automation/add_task_lambda.py"

# Check if add_task_lambda.py exists in the automation directory
if [ ! -f "$LAMBDA_PYTHON_FILE" ]; then
    echo "Error: add_task_lambda.py not found in automation directory!"
    exit 1
fi

# Make sure the function does not already exist
if aws lambda get-function --function-name CreateTask >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

# Get the IAM role ARN (ensure the role exists)
ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)

# Zip the add_task_lambda.py script
zip add_task_lambda.zip "$LAMBDA_PYTHON_FILE"

# Create the Add Task Lambda function
aws lambda create-function --function-name CreateTask \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://add_task_lambda.zip \
  --handler add_task_lambda.lambda_handler

# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name CreateTask  

# Publish a version of the function
aws lambda publish-version --function-name CreateTask

echo "Add Task Lambda function created and version published."

