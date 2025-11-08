import os
from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
)
from constructs import Construct

class BackendStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        reports_bucket: s3.Bucket,
        qa_table: dynamodb.Table,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda execution role
        lambda_role = iam.Role(
            self, "BackendLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            ]
        )

        # Grant permissions
        reports_bucket.grant_read_write(lambda_role)
        qa_table.grant_read_write_data(lambda_role)
        
        # Bedrock permissions
        lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeAgent"],
            resources=["*"]
        ))
        
        # HealthLake permissions
        lambda_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "healthlake:ReadResource",
                "healthlake:SearchWithGet",
                "healthlake:SearchWithPost",
                "healthlake:DescribeFHIRDatastore"
            ],
            resources=["*"]
        ))

        # Lambda function
        backend_lambda = _lambda.DockerImageFunction(
            self, "BackendFunction",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="../backend",
                file="Dockerfile"
            ),
            timeout=Duration.seconds(900),
            memory_size=1024,
            role=lambda_role,
            environment={
                "AWS_REGION": os.environ.get("AWS_REGION", "us-west-2"),
                "REPORTS_BUCKET": reports_bucket.bucket_name,
                "QA_TABLE": qa_table.table_name,
            }
        )

        # API Gateway
        api = apigw.RestApi(
            self, "BackendAPI",
            rest_api_name="HealthLake Backend API",
            description="FastAPI backend for HealthLake AI Assistant",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=["*"]
            )
        )

        # Lambda integration
        integration = apigw.LambdaIntegration(backend_lambda)
        
        # Proxy all requests to Lambda
        api.root.add_proxy(
            default_integration=integration,
            any_method=True
        )

        # Output API URL
        self.api_url = api.url
        CfnOutput(self, "ApiUrl", value=self.api_url)
