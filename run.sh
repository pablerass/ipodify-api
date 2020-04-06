#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export FLASK_APP=ipodify_api.wsgi:app
export FLASK_ENV=development

pushd $DIR
flask run --port=5001
popd