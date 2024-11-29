#!/bin/bash

# Make scripts executable
chmod +x ./automation/create_dynamodb_table.sh
chmod +x ./automation/create_add_tasks_lambda.sh
chmod +x ./automation/create_delete_task_lambda.sh
chmod +x ./automation/create_view_lambda.sh
chmod +x ./automation/create_task_manager_lambda.sh  

# Execute each script
echo "Running create_dynamodb_table.sh..."
./automation/create_dynamodb_table.sh
if [ $? -eq 0 ]; then
    echo "DynamoDB table creation script ran successfully."
else
    echo "Error running create_dynamodb_table.sh"
    exit 1
fi

echo "Running create_add_tasks_lambda.sh..."
./automation/create_add_tasks_lambda.sh
if [ $? -eq 0 ]; then
    echo "Add tasks Lambda function creation ran successfully."
else
    echo "Error running create_add_tasks_lambda.sh"
    exit 1
fi

echo "Running create_delete_task_lambda.sh..."
./automation/create_delete_task_lambda.sh
if [ $? -eq 0 ]; then
    echo "Delete task Lambda function creation ran successfully."
else
    echo "Error running create_delete_task_lambda.sh"
    exit 1
fi

echo "Running create_view_lambda.sh..."
./automation/create_view_lambda.sh
if [ $? -eq 0 ]; then
    echo "View Lambda function creation ran successfully."
else
    echo "Error running create_view_lambda.sh"
    exit 1
fi

echo "Running create_task_manager_lambda.sh..."  # New line for the task manager Lambda function creation
./automation/create_task_manager_lambda.sh
if [ $? -eq 0 ]; then
    echo "Task Manager Lambda function creation ran successfully."
else
    echo "Error running create_task_manager_lambda.sh"
    exit 1
fi

echo "All scripts ran successfully!"

write a script to delete everything created in this script
