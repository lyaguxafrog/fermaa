#!/bin/bash


if [[ $1 = 'pip' ]]; then
    rm -rf .devcontainer/requirements.txt
    pip install -r requirements.txt
    cat requirements.txt >> .devcontainer/requirements.txt
fi

if [[ $1 = 'run' ]]; then
    gunicorn -w 4 -b 0.0.0.0:8080 dmanage:app
fi

if [[ $1 = 'debug' ]]; then
    python dmanage.py debug
fi

if [[ $1 = 'cu' ]]; then
    python dmanage.py create-user
fi


if [[ $1 = 'migrate' ]]; then
    flask db migrate -m "$2"
    flask db upgrade
fi
