#!/bin/bash
# AWS credentials should be configured via AWS CLI or environment variables
# Run: aws configure
# Or set: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
export AWS_PAGER=""
export AWS_DEFAULT_REGION="us-west-2"

aws s3api get-bucket-tagging --bucket question1-bucket-908027381531
