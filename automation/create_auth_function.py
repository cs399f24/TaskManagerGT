#!/bin/bash

# Variables
FUNCTION_NAME="authFunction"
HANDLER="auth_function.lambda_handler"
ROLE_NAME="LabRole"
ZIP_FILE="auth_function.zip"
RUNTIME="python3.9"
REGION="us-east-1"

# Check if the role exists and get its ARN
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text 2>/dev/null)

if [ -z "$ROLE_ARN" ]; then
    echo "Role $ROLE_NAME does not exist. Please create the role and try again."
    exit 1
fi

# Create ZIP file for Lambda function
echo "Creating ZIP file..."
zip -r $ZIP_FILE auth_function.py > /dev/null

# Check if the function already exists
FUNCTION_EXISTS=$(aws lambda get-function --function-name $FUNCTION_NAME 2>/dev/null)

if [ -n "$FUNCTION_EXISTS" ]; then
    echo "Function $FUNCTION_NAME already exists. Updating the code..."
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb://$ZIP_FILE \
        --region $REGION
else
    echo "Creating the Lambda function $FUNCTION_NAME..."
    aws lambda create-function \
        --function-name $FUNCTION_NAME \
        --runtime $RUNTIME \
        --role $ROLE_ARN \
        --handler $HANDLER \
        --zip-file fileb://$ZIP_FILE \
        --region $REGION
fi

# Clean up
echo "Cleaning up..."
rm $ZIP_FILE

echo "Done!"

