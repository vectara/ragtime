# Argument to be passed to the Python script inside the Docker container
BOT_NAME=$1

# Build docker container
docker build -f Dockerfile . --tag=ragtime-bot:latest

# remove old container if it exists
docker container inspect ragtime-bot &>/dev/null && docker rm -f ragtime-bot

# Run the container
if [ -z "$RUN_BOT_ARG" ]; then
  docker run -d -v ./data/convo.db:/app/data/convo.db --env-file ./.env --name ragtime-bot ragtime-bot
else
  docker run -d -v "$(pwd)/data/convo.db:/app/data/convo.db" --env-file ./.env --name ragtime-bot ragtime-bot python main.py "$BOT_NAME"
fi