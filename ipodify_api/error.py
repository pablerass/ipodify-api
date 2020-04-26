# -*- coding: utf-8 -*-
"""Ipodify error management application."""
# TUNE: All this module looks like crap and its is
from flask import abort, jsonify, make_response


def handle_http_exception(e):
    """Return json output of exception."""
    return _jsonify_error(message=e.name, status_code=e.code), e.code


def abort_with_message(message, status_code):
    """Abort with specific message format."""
    return abort(make_response(_jsonify_error(message, status_code), status_code))


def _jsonify_error(message, status_code):
    """Return json output of the error."""
    # TUNE: Probably returning the status code is not the best approach
    return jsonify(error=status_code, text=message)
