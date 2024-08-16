import sys
import os

# Get the path to the directory containing the main.py file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

# Now you can import from the main.py file
from main import converse_wrapper
import boto3


client = boto3.client('bedrock-runtime')
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


# Example usage:
response = converse_wrapper(
    bedrock_client= client,
    model_id=MODEL_ID,
    messages=[{'role': 'user', 'content': [{'text': 'Create a list of 3 pop songs.'}]}],
    streaming=True
)


stream = response.get('stream')
if stream:
    for event in stream:
        if 'messageStart' in event:
            print(f"\nRole: {event['messageStart']['role']}")
        if 'contentBlockDelta' in event:
            print(event['contentBlockDelta']['delta']['text'], end="")
        if 'messageStop' in event:
            print(f"\nStop reason: {event['messageStop']['stopReason']}")
        if 'metadata' in event:
            metadata = event['metadata']
            if 'usage' in metadata:
                print("\nToken usage")
                print(f"Input tokens: {metadata['usage']['inputTokens']}")
                print(f"Output tokens: {metadata['usage']['outputTokens']}")
                print(f"Total tokens: {metadata['usage']['totalTokens']}")
            if 'metrics' in event['metadata']:
                print(f"Latency: {metadata['metrics']['latencyMs']} milliseconds")
    