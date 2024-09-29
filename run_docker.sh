#!/bin/bash

# Argument to be passed to the Python script inside the Docker container
BOT_NAME=$1

# Network name
NETWORK_NAME=ragtime-net

# Create Docker network if it doesn't exist
docker network inspect $NETWORK_NAME &>/dev/null || docker network create $NETWORK_NAME

# Build docker container
docker build -f Dockerfile . --tag=ragtime-bot:latest

# Remove old container if it exists
docker container inspect ragtime-bot &>/dev/null && docker rm -f ragtime-bot

# Run the ragtime-bot container on the same network
if [ -z "$RUN_BOT_ARG" ]; then
  docker run -d \
    --network=$NETWORK_NAME \
    -v "$(pwd)/data/convo.db:/app/data/convo.db" \
    --env-file ./.env \
    --name ragtime-bot \
    ragtime-bot
else
  docker run -d \
    --network=$NETWORK_NAME \
    -v "$(pwd)/data/convo.db:/app/data/convo.db" \
    --env-file ./.env \
    --name ragtime-bot \
    ragtime-bot python main.py "$BOT_NAME"
fi

# Remove old redis-server container if it exists
docker container inspect redis-server &>/dev/null && docker rm -f redis-server

# Run redis-server on the same network
docker run -d \
  --network=$NETWORK_NAME \
  -p 6379:6379 \
  --name redis-server \
  redis
