# Argument to be passed to the Python script inside the Docker container
BOT_NAME=$1

docker build -f Dockerfile . --tag=ask-vectara-slack-bot:latest
# remove old container if it exists
docker container inspect avectara-sbot &>/dev/null && docker rm -f avectara-sbot
if [ -z "$RUN_BOT_ARG" ]; then
  docker run -d -v ./data/convo.db:/app/data/convo.db --env-file ./.env --name avectara-sbot ask-vectara-slack-bot
else
  docker run -d -v "$(pwd)/data/convo.db:/app/data/convo.db" --env-file ./.env --name avectara-sbot ask-vectara-sbot python main.py "$BOT_NAME"
fi