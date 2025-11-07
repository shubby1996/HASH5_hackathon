import boto3
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

logs = boto3.client('logs', region_name='us-west-2')

# Get recent log streams
streams = logs.describe_log_streams(
    logGroupName='/aws/lambda/HealthLakeQueryFunction',
    orderBy='LastEventTime',
    descending=True,
    limit=5
)

print("Recent Lambda Executions:\n")

for stream in streams['logStreams']:
    stream_name = stream['logStreamName']
    print(f"\n{'='*80}")
    print(f"Stream: {stream_name}")
    print('='*80)
    
    events = logs.get_log_events(
        logGroupName='/aws/lambda/HealthLakeQueryFunction',
        logStreamName=stream_name,
        limit=100
    )
    
    for event in events['events']:
        msg = event['message']
        if 'ERROR' in msg or 'Traceback' in msg or 'Exception' in msg:
            print(msg)
