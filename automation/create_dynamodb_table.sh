# Check if the table already exists
if aws dynamodb describe-table --table-name Tasks >/dev/null 2>&1; then
    echo "Table Already Exists"
    exit 0
fi

# Create the Tasks table
aws dynamodb create-table \
    --table-name Tasks \
    --key-schema \
        AttributeName=UserId,KeyType=HASH \
        AttributeName=TaskId,KeyType=RANGE \
    --attribute-definitions \
        AttributeName=UserId,AttributeType=S \
        AttributeName=TaskId,AttributeType=S \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 > /dev/null || exit 1

# Create global secondary index (optional, for querying tasks by status)
aws dynamodb update-table \
    --table-name Tasks \
    --attribute-definitions \
        AttributeName=Status,AttributeType=S \
    --global-secondary-index-updates \
        "[{\"Create\":{\"IndexName\":\"StatusIndex\",\"KeySchema\":[{\"AttributeName\":\"Status\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"UserId\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"},\"ProvisionedThroughput\":{\"ReadCapacityUnits\":5,\"WriteCapacityUnits\":5}}}]"

echo "DONE"
