import os
import json
import boto3
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, as_completed

_AWS_LAMBDA_FUNCTION_NAME = os.getenv("AWS_LAMBDA_FUNCTION_NAME")
_AWS_LAMBDA_FUNCTION_VERSION = os.getenv("AWS_LAMBDA_FUNCTION_VERSION")


def generate_custom_reply(event, flag):
    """Function to generate custom response 
    for warming call for lambda handler

    Args:
        event (_type_): Lambda Event
        flag (_type_): Key to identify event as warming event

    Returns:
        _type_: None
    """
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": {
            "eventFlag": event.get(flag),
            "status": "warmed up",
            "functionName": _AWS_LAMBDA_FUNCTION_NAME,
            "functionVersion": _AWS_LAMBDA_FUNCTION_VERSION
        },
        "headers": {
            "content-type": "application/json"
        }
    }


def call_function_concurrently(concurrent_calls: int, flag: str):
    """Function to call Lambda concurrently
    This is using Threadpool executor for calling Lmabdas concurrently
    so that we make sure Lmabda isn't available to pick
    next warming request concurrently.

    Args:
        concurrent_calls (int): Number of concurrent calls for warming lambda
        flag (str): Flag event for Lambda to identify warming call
    """
    client = boto3.client('lambda')
    data = json.dumps({flag: True, "concurrency": 1})
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as exe:
        map_ = []
        for _ in range(concurrent_calls-1):
            map_.append(
                exe.submit(client.invoke, FunctionName=_AWS_LAMBDA_FUNCTION_NAME,
                           Payload=data.encode("utf-8"),
                           Qualifier=_AWS_LAMBDA_FUNCTION_VERSION)
            )
        for f in as_completed(map_):
            try:
                print(f.result())
            except Exception as e:  # skipcq
                print(f"got exception while executing function: {e}")


def warmer(flag="warmer", _concurrency=1):
    """This decorator adds and additional layer
    on the top of your callable for warming 
    lambda

    Args:
        flag (str, optional): key in event json to check if the event is for warming. Defaults to "warmer".
    """
    def decorator(func):
        @wraps(func)
        def inner_wrapper(event, context, *args, **kwargs):
            if event.get(flag):
                concurrency = event.get("concurrency") or _concurrency
                if concurrency > 1:
                    call_function_concurrently(concurrency, flag)
                print(
                    f"warming {_AWS_LAMBDA_FUNCTION_NAME}:{_AWS_LAMBDA_FUNCTION_VERSION} with custom event")
                return generate_custom_reply(event=event, flag=flag)
            return func(event, context, *args, **kwargs)
        return inner_wrapper
    return decorator
