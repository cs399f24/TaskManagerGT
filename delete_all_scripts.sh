#!/bin/bash

# Make scripts executable
chmod +x ./automation/delete_dynamodb_table.sh
chmod +x ./automation/delete_add_tasks_lambda.sh
chmod +x ./automation/delete_delete_task_lambda.sh
chmod +x ./automation/delete_view_lambda.sh
chmod +x ./automation/delete_task_manager_lambda.sh  

# Execute each script
echo "Running delete_dynamodb_table.sh..."
./automation/delete_dynamodb_table.sh
if [ $? -eq 0 ]; then
    echo "DynamoDB table deletion script ran successfully."
else
    echo "Error running delete_dynamodb_table.sh"
    exit 1
fi

echo "Running delete_add_tasks_lambda.sh..."
./automation/delete_add_tasks_lambda.sh
if [ $? -eq 0 ]; then
    echo "Add tasks Lambda function deletion ran successfully."
else
    echo "Error running delete_add_tasks_lambda.sh"
    exit 1
fi

echo "Running delete_delete_task_lambda.sh..."
./automation/delete_delete_task_lambda.sh
if [ $? -eq 0 ]; then
    echo "Delete task Lambda function deletion ran successfully."
else
    echo "Error running delete_delete_task_lambda.sh"
    exit 1
fi

echo "Running delete_view_lambda.sh..."
./automation/delete_view_lambda.sh
if [ $? -eq 0 ]; then
    echo "View Lambda function deletion ran successfully."
else
    echo "Error running delete_view_lambda.sh"
    exit 1
fi

echo "Running delete_task_manager_lambda.sh..."  # Line for the task manager Lambda function deletion
./automation/delete_task_manager_lambda.sh
if [ $? -eq 0 ]; then
    echo "Task Manager Lambda function deletion ran successfully."
else
    echo "Error running delete_task_manager_lambda.sh"
    exit 1
fi

echo "All delete scripts ran successfully!"

