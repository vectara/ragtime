#!/bin/bash

if [ -f .env ]; then
    set -o allexport
    source .env
    set +o allexport
else
    echo ".env file not found!"
    exit 1
fi

if [ "$ENABLE_AGENTIC_RAG" == "True" ]; then
    CONTAINER_NAME="agentic-rag-bot"
else
    CONTAINER_NAME="ragtime"
fi

BOT_NAME=$1

NETWORK_NAME=ragtime-net

docker network inspect $NETWORK_NAME &>/dev/null || docker network create $NETWORK_NAME

docker build -f Dockerfile . --tag=${CONTAINER_NAME}:latest

docker container inspect ${CONTAINER_NAME} &>/dev/null && docker rm -f ${CONTAINER_NAME}

if [ -z "$BOT_NAME" ]; then
  docker run -d \
    --network=$NETWORK_NAME \
    -v "$(pwd)/data/convo.db:/app/data/convo.db" \
    -p 5000:5000 \
    --env-file ./.env \
    --name ${CONTAINER_NAME} \
    ${CONTAINER_NAME}
else
  docker run -d \
    --network=$NETWORK_NAME \
    -v "$(pwd)/data/convo.db:/app/data/convo.db" \
    -p 5000:5000 \
    --env-file ./.env \
    --name ${CONTAINER_NAME} \
    ${CONTAINER_NAME} python main.py "$BOT_NAME"
fi

if [ "$ENABLE_AGENTIC_RAG" == "True" ]; then

    docker container inspect redis-server &>/dev/null && docker rm -f redis-server

    docker run -d \
      --network=$NETWORK_NAME \
      -p 6379:6379 \
      --name redis-server \
      redis
else
    echo "Skipping redis-server container as ENABLE_AGENTIC_RAG is not set to true."
fi
