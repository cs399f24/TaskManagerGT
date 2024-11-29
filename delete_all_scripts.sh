#!/bin/bash

# Delete DynamoDB table
echo "Deleting DynamoDB table..."
aws dynamodb delete-table --table-name <DYNAMODB_TABLE_NAME>
if [ $? -eq 0 ]; then
    echo "DynamoDB table deleted successfully."
else
    echo "Error deleting DynamoDB table."
    exit 1
fi

# Delete Lambda functions
echo "Deleting add tasks Lambda function..."
aws lambda delete-function --function-name <ADD_TASKS_LAMBDA_NAME>
if [ $? -eq 0 ]; then
    echo "Add tasks Lambda function deleted successfully."
else
    echo "Error deleting add tasks Lambda function."
    exit 1
fi

echo "Deleting delete task Lambda function..."
aws lambda delete-function --function-name <DELETE_TASK_LAMBDA_NAME>
if [ $? -eq 0 ]; then
    echo "Delete task Lambda function deleted successfully."
else
    echo "Error deleting delete task Lambda function."
    exit 1
fi

echo "Deleting view Lambda function..."
aws lambda delete-function --function-name <VIEW_LAMBDA_NAME>
if [ $? -eq 0 ]; then
    echo "View Lambda function deleted successfully."
else
    echo "Error deleting view Lambda function."
    exit 1
fi

echo "Deleting task manager Lambda function..."
aws lambda delete-function --function-name <TASK_MANAGER_LAMBDA_NAME>
if [ $? -eq 0 ]; then
    echo "Task Manager Lambda function deleted successfully."
else
    echo "Error deleting task manager Lambda function."
    exit 1
fi

echo "Cleanup complete! All resources have been deleted."
