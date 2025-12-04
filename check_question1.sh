#!/bin/bash
# AWS credentials should be configured via AWS CLI or environment variables
# Run: aws configure
# Or set: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
export AWS_PAGER=""
export AWS_DEFAULT_REGION="us-west-2"

echo "=== Checking question1 tag value ==="
TAG_VALUE=$(aws s3api get-bucket-tagging --bucket question1-bucket-908027381531 --query 'TagSet[?Key==`question1`].Value' --output text)

echo "Current value: $TAG_VALUE"

if [ "$TAG_VALUE" = "complete" ]; then
    echo "✓ SUCCESS! The tag has been changed to 'complete'"
elif [ "$TAG_VALUE" = "incomplete" ]; then
    echo "✗ The tag is still 'incomplete' - needs to be updated"
else
    echo "? Unexpected value: $TAG_VALUE"
fi
