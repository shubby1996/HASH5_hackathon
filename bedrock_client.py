import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

class BedrockClient:
    def __init__(self, region_name=None):
        self.region = region_name or os.getenv('AWS_REGION', 'us-east-1')
        self.client = boto3.client('bedrock-runtime', region_name=self.region)
    
    def invoke_claude(self, prompt, max_tokens=1000):
        response = self.client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}]
            })
        )
        result = json.loads(response['body'].read())
        return result['content'][0]['text']

if __name__ == "__main__":
    client = BedrockClient()
    response = client.invoke_claude("What is AWS Bedrock?")
    print(response)
