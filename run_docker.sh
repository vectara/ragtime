docker build -f Dockerfile . --tag=ask-vectara-slack-bot:latest
# remove old container if it exists
docker container inspect avectara-sbot &>/dev/null && docker rm -f avectara-sbot
docker run -d -v ./data/convo.db:/app/data/convo.db --env-file ./.env --name avectara-sbot ask-vectara-slack-bot