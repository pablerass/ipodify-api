#!/usr/bin/env python3
"""Ipodify wsgi interface."""
import logging

from .app import create_app


logging.basicConfig(level=logging.DEBUG)
# TODO: Remove inject specific logging
app = create_app()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
