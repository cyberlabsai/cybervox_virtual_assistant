#!/bin/bash

source bin/settings.sh

if [[ $DOCKER_COMMON_DIR == "" ]];then
    DOCKER_COMMON_DIR="/tmp/docker-common"
fi
[[ -d $DOCKER_COMMON_DIR ]] || mkdir -p $DOCKER_COMMON_DIR

export $(cat .env)

if [[ $PORT == "" ]];then
    echo "You didn't set \`PORT\` environment variable. It's okay,"
    echo "but this container won't listen to anything from outside."
    PORTARG=""
else
    PORTARG="-p $PORT:$PORT"
fi

docker-compose run \
    -v $DOCKER_COMMON_DIR:/docker-common \
    -v $PWD:/app/src \
    $PORTARG \
    --entrypoint /bin/bash \
    $PROJECT_NAME $*