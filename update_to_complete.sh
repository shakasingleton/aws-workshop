#!/bin/bash
# AWS credentials should be configured via AWS CLI or environment variables
# Run: aws configure
# Or set: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
export AWS_PAGER=""
export AWS_DEFAULT_REGION="us-west-2"

echo "Updating question1 tag to 'complete'..."

aws s3api put-bucket-tagging \
  --bucket question1-bucket-908027381531 \
  --tagging 'TagSet=[{Key=aws:cloudformation:stack-name,Value=participant-account},{Key=aws:cloudformation:logical-id,Value=Question1Bucket},{Key=aws:cloudformation:stack-id,Value=arn:aws:cloudformation:us-west-2:908027381531:stack/participant-account/be5c5500-d018-11f0-85d9-06ed98ed0a47},{Key=question1,Value=complete}]'

echo ""
echo "Verifying the update..."
TAG_VALUE=$(aws s3api get-bucket-tagging --bucket question1-bucket-908027381531 --query 'TagSet[?Key==`question1`].Value' --output text)

echo "New value: $TAG_VALUE"

if [ "$TAG_VALUE" = "complete" ]; then
    echo "✓ SUCCESS! Question 1 is now marked as complete!"
else
    echo "✗ Update failed. Current value: $TAG_VALUE"
fi
