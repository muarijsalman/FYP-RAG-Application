import inspect
from typing import Annotated, List
from fastapi import Form
import os

def as_form(cls):
    new_params = [
        inspect.Parameter(
            field_name,
            inspect.Parameter.POSITIONAL_ONLY,
            default=model_field.default,
            annotation=Annotated[model_field.annotation, *model_field.metadata, Form()],
        )
        for field_name, model_field in cls.model_fields.items()
    ]

    cls.__signature__ = cls.__signature__.replace(parameters=new_params)

    return cls

def get_env_var(key: str):
    if key in os.environ:
        return os.environ[key]
    raise ValueError(f"Missing Env Param: {key}")

def get_pinecone_api_key():
    return get_env_var("PINECONE_API_KEY")

def get_pinecone_index_name():
    return get_env_var("PINECONE_INDEX_NAME")

def get_aws_secret_key():
    return get_env_var("AWS_SECRET_KEY")

def get_aws_access_id():
    return get_env_var("AWS_ACCESS_ID")

def get_aws_bucket_name():
    return get_env_var("AWS_BUCKET_NAME")

def get_aws_endpoint_url():
    return get_env_var("AWS_ENDPOINT_URL")

def get_aws_public_url():
    return get_env_var("AWS_PUBLIC_URL")

def batch_inputs(data: List, batch_size: int = 32):
    for i in range(0, len(data), batch_size):
        yield data[i:i+batch_size]