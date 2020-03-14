#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export FLASK_APP=ipodify_api.app:app
export FLASK_ENV=development

pushd $DIR
flask run --port=5001
popd