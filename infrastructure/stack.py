from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    Duration,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct
import os

class InfrastructureStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # DynamoDB Table
        events_table = dynamodb.Table(
            self, "EventsTable",
            partition_key=dynamodb.Attribute(
                name="eventId",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # Lambda Layer for dependencies
        backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
        
        # Lambda function
        api_lambda = _lambda.Function(
            self, "EventsApiFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda_handler.handler",
            code=_lambda.Code.from_asset(
                backend_path,
                bundling={
                    "image": _lambda.Runtime.PYTHON_3_11.bundling_image,
                    "command": [
                        "bash", "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
                    ]
                }
            ),
            environment={
                "DYNAMODB_TABLE": events_table.table_name
            },
            timeout=Duration.seconds(30),
            memory_size=512
        )
        
        # Grant Lambda permissions to DynamoDB
        events_table.grant_read_write_data(api_lambda)
        
        # API Gateway
        api = apigw.LambdaRestApi(
            self, "EventsApi",
            handler=api_lambda,
            proxy=True,
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=["*"]
            )
        )
        
        # Outputs
        CfnOutput(
            self, "ApiUrl",
            value=api.url,
            description="API Gateway URL"
        )
        
        CfnOutput(
            self, "TableName",
            value=events_table.table_name,
            description="DynamoDB Table Name"
        )
