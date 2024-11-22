#!/bin/bash

# Define region and resource names
REGION="us-east-1"
API_NAME="TaskManagerAPI"
LAMBDA_FUNCTION="taskManagerLambdaFunction"
S3_BUCKET_NAME="task-manager-app-bucket"
STATIC_WEBSITE_DIR="path/to/your/webapp"  # Directory containing your static website files (HTML, CSS, JS)

# 1. Check if the API already exists in API Gateway
echo "Checking if API already exists..."
API_EXISTS=$(aws apigateway get-rest-apis --region $REGION --query "items[?name=='$API_NAME'].id" --output text)

if [ "$API_EXISTS" == "None" ]; then
    echo "Creating API Gateway..."
    RESPONSE=$(aws apigateway create-rest-api \
        --name $API_NAME \
        --description "Task Manager API" \
        --endpoint-configuration types=REGIONAL \
        --region $REGION)
    API_ID=$(echo $RESPONSE | jq -r .id)
else
    echo "API Gateway '$API_NAME' already exists."
    API_ID=$API_EXISTS
fi

# 2. Set up resources for API Gateway (e.g., /task resource)
ROOT_ID=$(aws apigateway get-resources --rest-api-id $API_ID --region $REGION --query "items[?path=='/'].id" --output text)
TASK_RESOURCE_ID=$(aws apigateway create-resource \
    --rest-api-id $API_ID \
    --parent-id $ROOT_ID \
    --path-part 'task' \
    --region $REGION \
    --query "id" --output text)

# 3. Setup GET and POST Methods for /task
aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $TASK_RESOURCE_ID \
    --http-method GET \
    --authorization-type NONE \
    --region $REGION

aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $TASK_RESOURCE_ID \
    --http-method POST \
    --authorization-type NONE \
    --region $REGION

# 4. Lambda Integration for Task Resource (assuming Lambda function is already created)
LAMBDA_ARN=$(aws lambda get-function --function-name $LAMBDA_FUNCTION --region $REGION --query "Configuration.FunctionArn" --output text)
URI="arn:aws:apigateway:$REGION:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations"

aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $TASK_RESOURCE_ID \
    --http-method POST \
    --integration-http-method POST \
    --type AWS_PROXY \
    --uri $URI \
    --region $REGION

aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $TASK_RESOURCE_ID \
    --http-method GET \
    --integration-http-method GET \
    --type AWS_PROXY \
    --uri $URI \
    --region $REGION

# 5. Deploy API Gateway
aws apigateway create-deployment \
    --rest-api-id $API_ID \
    --stage-name prod \
    --region $REGION

# 6. Set up S3 bucket for static website hosting
echo "Setting up S3 bucket for static website hosting..."

# Create the S3 bucket (make sure the bucket name is globally unique)
aws s3 mb s3://$S3_BUCKET_NAME --region $REGION

# Enable static website hosting on the bucket
aws s3 website s3://$S3_BUCKET_NAME/ --index-document index.html --error-document error.html --region $REGION

# Upload the website files to the S3 bucket
aws s3 sync $STATIC_WEBSITE_DIR/ s3://$S3_BUCKET_NAME/ --region $REGION

# 7. Output the public URL of the S3 website
S3_URL="http://$S3_BUCKET_NAME.s3-website-$REGION.amazonaws.com"
echo "Static website deployed to S3 at: $S3_URL"

# 8. Output the API URL
API_URL="https://$API_ID.execute-api.$REGION.amazonaws.com/prod/task"
echo "API URL: $API_URL"

echo "Deployment complete!"
