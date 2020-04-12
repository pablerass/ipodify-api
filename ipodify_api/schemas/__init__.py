# -*- coding: utf-8 -*-
"""Manage payload schemas."""
import json
import os

from flask import request
from functools import wraps
from jsonschema import validate, ValidationError, RefResolver

from ..error import abort_with_message


SCHEMA_FILES_PATH = os.path.dirname(os.path.abspath(__file__))


def _get_schema_file_name(schema_name):
    """Get schema file name."""
    return os.path.join(SCHEMA_FILES_PATH, f"{schema_name}.schema.json")


def validate_schema_data(data, schema_name):
    """Validate data against an schema."""
    with open(_get_schema_file_name(schema_name), 'r') as f:
        schema = json.load(f)
        resolver = RefResolver(
            base_uri=f"file://{SCHEMA_FILES_PATH}/",
            referrer=schema
        )
        validate(data, schema, resolver=resolver)


def body_schema(schema_name):
    """Validate payload schema."""
    def caller(func):
        @wraps(func)
        def wrapper(*kargs, **kwargs):
            try:
                validate_schema_data(request.json, schema_name)
                return func(*kargs, **kwargs)
            except ValidationError as e:
                # TODO: Improve response message
                return abort_with_message(e.message, 400)
        return wrapper
    return caller
