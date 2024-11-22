if aws lambda get-function --function-name deleteTaskFunction >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)

# Make sure to zip the delete_task_lambda.py script
zip delete_task_lambda.zip delete_task_lambda.py

# Create the Delete Task Lambda function
aws lambda create-function --function-name deleteTaskFunction \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://delete_task_lambda.zip \
  --handler delete_task_lambda.lambda_handler

# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name deleteTaskFunction  

# Publish a version of the function
aws lambda publish-version --function-name deleteTaskFunction
