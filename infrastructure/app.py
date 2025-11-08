#!/usr/bin/env python3
import os
from aws_cdk import App, Environment
from dotenv import load_dotenv
from stacks.frontend_stack import FrontendStack
from stacks.backend_stack import BackendStack
from stacks.storage_stack import StorageStack

load_dotenv()

app = App()

env = Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT", os.environ.get("AWS_ACCOUNT_ID")),
    region=os.environ.get("AWS_REGION", "us-west-2")
)

# Storage stack (DynamoDB + S3)
storage_stack = StorageStack(app, "HealthLakeStorageStack", env=env)

# Backend stack (Lambda + API Gateway)
backend_stack = BackendStack(
    app, "HealthLakeBackendStack",
    env=env,
    reports_bucket=storage_stack.reports_bucket,
    qa_table=storage_stack.qa_table
)

# Frontend stack (S3 + CloudFront)
frontend_stack = FrontendStack(
    app, "HealthLakeFrontendStack",
    env=env,
    api_url=backend_stack.api_url
)

app.synth()
