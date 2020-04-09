# -*- coding: utf-8 -*-
"""Manage payload schemas."""
import json
import os

from flask import request
from functools import wraps
from jsonschema import validate


def _get_schema_file_name(schema_name):
    """Get schema file name."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{schema_name}.schema.json")


def validate_schema_data(data, schema_name):
    """Validate data against an schema."""
    with open(_get_schema_file_name(schema_name), 'r') as f:
         return validate(data, json.load(f))


def payload_schema(schema_name):
    """Validate payload schema."""
    def caller(func):
        @wraps(func)
        def wrapper(*kargs, **kwargs):
            validate_schema_data(request.json, schema_name)
            return func(*kargs, **kwargs)
        return wrapper
    return caller
