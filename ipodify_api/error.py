# -*- coding: utf-8 -*-
"""Ipodify error management application."""
from flask import abort, jsonify, make_response


def handle_http_exception(e):
    """Return json output of exception."""
    return _jsonify_error(e.code, e.name)


def abort_with_message(message, status_code):
    """Abort with specific message format."""
    return abort(make_response(_jsonify_error(message, status_code), status_code))


def _jsonify_error(message, status_code):
    """Return json output of the error."""
    return jsonify(error=status_code, text=message)
