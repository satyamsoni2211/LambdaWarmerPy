import os
from functools import wraps

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


def warmer(flag="warmer"):
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
                print(
                    f"warming {_AWS_LAMBDA_FUNCTION_NAME}:{_AWS_LAMBDA_FUNCTION_VERSION} with custom event")
                return generate_custom_reply(event=event, flag=flag)
            return func(event, context, *args, **kwargs)
        return inner_wrapper
    return decorator
