#!/bin/bash

if [[ $1 = 'config' ]]; then
    rm -rf kernel/.devcontainer
    rm -rf kernel/.vscode
    rm -rf docs/
    rm -rf README.md
    cat .env.example >> kernel/.env
    echo ".env создан"
    echo "Обязательно смените SECRET_KEY"
    echo "Так же не забудьте настроить SMTP и SMS"
fi

if [[ $1 = 'deploy' ]]; then
	
    echo "Author: Adrian Makridenko | https://github.com/lyaguxafrog" > .author
    docker-compose up -d --build nginx

fi
