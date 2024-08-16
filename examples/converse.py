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
    bedrock_client=client,
    model_id=MODEL_ID,
    messages=[{'role': 'user', 'content': [{'text': 'Hello, how are you?'}]}],
    streaming=False
)

print(response['output']['message']['content'][0]['text'])