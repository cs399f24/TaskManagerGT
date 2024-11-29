#!/bin/bash

# Variables
BUCKET_NAME="aws-s3-task-manager-bucket-$(date +%s)" # Dynamic unique bucket name
REGION="us-east-1"                             # Change to your desired AWS region
INDEX_DOCUMENT="index.html"                    # Index document for static website hosting

# Step 1: Create S3 bucket (handle us-east-1 special case)
echo "Creating bucket: $BUCKET_NAME in region: $REGION..."
if [[ "$REGION" == "us-east-1" ]]; then
  CREATE_BUCKET_OUTPUT=$(aws s3api create-bucket \
    --bucket "$BUCKET_NAME" \
    --region "$REGION" 2>&1)
else
  CREATE_BUCKET_OUTPUT=$(aws s3api create-bucket \
    --bucket "$BUCKET_NAME" \
    --region "$REGION" \
    --create-bucket-configuration LocationConstraint="$REGION" 2>&1)
fi

if [[ $? -ne 0 ]]; then
  echo "Error creating bucket: $CREATE_BUCKET_OUTPUT"
  exit 1
fi
echo "Bucket $BUCKET_NAME created successfully."

# Step 2: Disable block public access settings
echo "Disabling block public access settings..."
aws s3api put-public-access-block \
  --bucket "$BUCKET_NAME" \
  --public-access-block-configuration BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false

if [[ $? -ne 0 ]]; then
  echo "Failed to disable block public access settings."
  exit 1
fi
echo "Block public access settings disabled."

# Step 3: Enable static website hosting
echo "Enabling static website hosting..."
aws s3 website s3://"$BUCKET_NAME"/ \
  --index-document "$INDEX_DOCUMENT"

if [[ $? -ne 0 ]]; then
  echo "Failed to enable static website hosting."
  exit 1
fi
echo "Static website hosting enabled with index document: $INDEX_DOCUMENT."

# Step 4: Retrieve bucket ARN
echo "Retrieving bucket ARN..."
BUCKET_ARN="arn:aws:s3:::$BUCKET_NAME"

# Step 5: Generate and apply bucket policy
echo "Applying bucket policy..."
POLICY=$(cat <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "$BUCKET_ARN/*"
        }
    ]
}
EOF
)

aws s3api put-bucket-policy \
  --bucket "$BUCKET_NAME" \
  --policy "$POLICY"

if [[ $? -ne 0 ]]; then
  echo "Failed to apply bucket policy."
  exit 1
fi
echo "Bucket policy applied successfully."

# Step 6: Add CORS policy
echo "Adding CORS policy..."
WEBSITE_URL="http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com"
CORS_POLICY_FILE="/tmp/cors-policy.json"

# Write the CORS policy to a file
cat > "$CORS_POLICY_FILE" <<EOF
{
    "CORSRules": [
        {
            "AllowedHeaders": [
                "*"
            ],
            "AllowedMethods": [
                "GET",
                "POST",
                "PUT"
            ],
            "AllowedOrigins": [
                "$WEBSITE_URL"
            ],
            "ExposeHeaders": [],
            "MaxAgeSeconds": 3000
        }
    ]
}
EOF

# Apply the CORS configuration
aws s3api put-bucket-cors \
  --bucket "$BUCKET_NAME" \
  --cors-configuration file://"$CORS_POLICY_FILE"

if [[ $? -ne 0 ]]; then
  echo "Failed to apply CORS policy."
  rm -f "$CORS_POLICY_FILE"  # Clean up
  exit 1
fi

# Clean up temporary file
rm -f "$CORS_POLICY_FILE"

echo "CORS policy applied successfully."

# Final Output
echo "Bucket $BUCKET_NAME has been successfully configured for static website hosting."
echo "Website URL: $WEBSITE_URL"
