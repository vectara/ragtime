# Ragtime

An open-source RAG bot for slack and discord using Vectara.
With this bot you can create a slack or Discord bot that is connected to your server and answers user questions by querying a Vectara corpus.

## Usage

- Mention the bot in a message to receive a reply.
- Send a direct message to the bot for a 1:1 conversation.
- The bot stores message and thread IDs to provide context-aware replies in threads or while replying.

## Example Commands
- Mention the bot: `@bot-name Your message here`
- Send a direct message: `Your message here`

## Installation

### Prerequisites

- Python 3.8 or higher

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vectara/ragtime.git
   cd ragtime
   
2. **Install the required dependencies:**
   ```bash
    pip3 install requirement.txt
   
3. **Create an `.env` file and copy the env variables name from the .env.example and replace with credentials.**


4. **Create Slack bot app in the slack by using the following steps.**
- **Create a Slack App**: Log in to your Slack workspace and navigate to the Slack API website. Click on "Your Apps" and then "Create New App." Provide a name for your app, select the workspace where you want to install it, and click "Create App."

- **Configure Basic Information**: In the app settings, you can configure various details such as the app name, icon, and description. Make sure to fill out the necessary information accurately.

- **Install the Bot to Your Workspace**: Once you've configured your app, navigate to the "Install App" section. Click on the "Install App to Workspace" button to add the bot to your Slack workspace. This step will generate an OAuth access token that you'll need to use to authenticate your bot.

- **Add User Token Scope**: To add user token scope, navigate to the "OAuth & Permissions" section in your app settings. Under the "OAuth Tokens for Your Workspace" section, you'll need to add  `app_mentions:read`, `channels:history`, `chat:write`, `chat:write.public`, `groups:history`, `im:history`, `mpim:history`, `mpim:read`, `mpim:write`, `users:read` scopes. Create the token and save it as `SLACK_BOT_TOKEN`.

- **APP Level Token**: Create an app level token with the `connection:write` scope. Save this token as SLACK_APP_TOKEN

- **Save Changes**: Make sure to save any changes you've made to your app settings and install/reinstall the bot to workplace.

5. **Create discord by navigating to [Discord Developer Portal Applications Page](https://discord.com/developers/applications).**
- Create a new application by clicking on the ‘New Application‘ button on the top-right corner.
- Go to the ‘Bot‘ page by selecting the ‘Bot‘ option from the left column.
- Copy the provided token and save it as `DiSCORD_BOT_TOKEN`.
- Choose ‘OAuth2’ from the left column and select the URL Generator.
- In the ‘Bot Permissions’ section at the bottom, select the necessary permissions.
- Choose the ‘bot’ option in the ‘Scope’ box, and the ‘BOT PERMISSIONS’ box will appear below it.
- Select ‘Read Message’, ‘Send Message’, and ‘Manage Message’ options.
- Copy the generated URL and paste it into your web browser. It will redirect you to the Discord page to add the bot to your server.

6. **Run the bot**
- To run the both bots execute the following command.
   ```bash
   python3 main.py
  
- To run only slack bot execute the following command.
   ```bash
   python3 main.py slack
  
- To run only discord bot execute the following command.
   ```bash
   python3 main.py discord
 
## Docker
**Build and Run with docker.**
   ```bash
   bash run_docker.sh
   
