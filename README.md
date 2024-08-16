# Amazon Bedrock Converse API Wrapper

## Overview

This wrapper provides a simplified interface for Amazon Bedrock's Converse API, supporting both standard and streaming modes. It streamlines the process of interacting with Amazon Bedrock's language models by providing a single function that can handle both synchronous and asynchronous (streaming) requests.

## Features

- Supports both standard and streaming API calls
- Handles all optional parameters for maximum flexibility
- Easy to switch between streaming and non-streaming modes
- Compatible with various Amazon Bedrock models

## Requirements

- Python 3.6+
- boto3 library

## Installation

Ensure you have boto3 installed:

```bash
pip install boto3
```

## Usage

1. Import the necessary libraries and the wrapper function:

```python
import boto3
from bedrock_converse_wrapper import converse_wrapper
```

2. Set up your AWS credentials (if not already configured)

3. Create a Bedrock client:

```python
bedrock_client = boto3.client(service_name='bedrock-runtime')
```

4. Use the wrapper function:

```python
response = converse_wrapper(
    bedrock_client,
    model_id='anthropic.claude-3-sonnet-20240229-v1:0',
    messages=[{"role": "user", "content": [{"text": "Hello, how are you?"}]}],
    streaming=True
)
```

## Function Signature

```python
def converse_wrapper(
    bedrock_client,
    model_id,
    messages,
    system_prompts=None,
    inference_config=None,
    additional_model_fields=None,
    streaming=True
)
```

## Parameters

- `bedrock_client` (required): The boto3 client for 'bedrock-runtime'.
- `model_id` (required): String identifier for the model to use.
- `messages` (required): List of message objects representing the conversation history.
- `system_prompts` (optional): List of system message objects.
- `inference_config` (optional): Dictionary containing inference configuration options.
- `additional_model_fields` (optional): Dictionary containing additional fields for the model request.
- `streaming` (optional): Boolean flag to enable streaming mode (default: True).

## Return Value

- For non-streaming calls (`streaming=False`): Returns the full response from the Bedrock Converse API.
- For streaming calls (`streaming=True`): Returns the response object from the Bedrock Converse Stream API, which includes a 'stream' key containing the event stream.

## Handling Streaming Responses

When using streaming mode, you need to process the event stream manually. Here's an example of how to handle the streaming response:

```python
response = converse_wrapper(bedrock_client, model_id, messages, streaming=True)
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
```

## Error Handling

The wrapper function will raise any ClientError exceptions that occur during the API call. It's recommended to implement appropriate try/except blocks when using this wrapper.

## Best Practices

1. Always set a reasonable `maxTokens` value in `inference_config` to control costs and response length.
2. Use `system_prompts` to set the context or behavior of the model.
3. Handle streaming responses appropriately by iterating over the response object.
4. Be mindful of rate limits and implement appropriate retry logic if necessary.

## Limitations

- This wrapper does not handle authentication or credential management. Ensure your AWS credentials are properly configured.
- It does not implement any caching or rate limiting. Implement these if needed for your use case.
- The wrapper does not validate the input parameters. Ensure you provide valid inputs according to the Bedrock API specifications.

## Example

Here's a complete example of how to use the wrapper:

```python
import boto3
from bedrock_converse_wrapper import converse_wrapper

model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
system_prompt = """You are an app that creates playlists for a radio station
  that plays rock and pop music. Only return song names and the artist."""
input_text = "Create a list of 3 pop songs."

messages = [{"role": "user", "content": [{"text": input_text}]}]
system_prompts = [{"text": system_prompt}]
inference_config = {"temperature": 0.5}
additional_model_fields = {"top_k": 200}

try:
    bedrock_client = boto3.client(service_name='bedrock-runtime')
    response = converse_wrapper(
        bedrock_client,
        model_id,
        messages,
        system_prompts=system_prompts,
        inference_config=inference_config,
        additional_model_fields=additional_model_fields,
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

except ClientError as err:
    print(f"An error occurred: {err.response['Error']['Message']}")
else:
    print(f"Finished conversation with model {model_id}.")
```

## Contributing

Contributions to improve the wrapper are welcome. Please submit a pull request or open an issue to discuss proposed changes.

## License

[BSD 3-Clause License]

## Disclaimer

This wrapper is not officially associated with Amazon Web Services. Use at your own risk and ensure compliance with AWS terms of service and Bedrock usage guidelines.