import boto3
from botocore.exceptions import ClientError


def converse_wrapper(
    bedrock_client,
    model_id,
    messages,
    system_prompts=None,
    inference_config=None,
    additional_model_fields=None,
    streaming=True
):
    """
    Wrapper function for Amazon Bedrock's Converse API, supporting both streaming and non-streaming responses.
    
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        messages (list): The messages to send.
        system_prompts (list, optional): The system prompts to send.
        inference_config (dict, optional): The inference configuration to use.
        additional_model_fields (dict, optional): Additional model fields to use.
        streaming (bool): Whether to use streaming API or not. Default is True.
    
    Returns:
        dict: A dictionary containing the response data.
    """
    # Prepare the request parameters
    params = {
        "modelId": model_id,
        "messages": messages
    }
    if system_prompts:
        params["system"] = system_prompts
    if inference_config:
        params["inferenceConfig"] = inference_config
    if additional_model_fields:
        params["additionalModelRequestFields"] = additional_model_fields

    try:
        if streaming:
            response = bedrock_client.converse_stream(**params)
            return response
        else:
            return bedrock_client.converse(**params)
    except ClientError as err:
        f"A client error occurred:  {err.response['Error']['Message']}"]
        raise


