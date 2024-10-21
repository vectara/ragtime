# Ragtime

An open-source RAG bot for Slack and Discord using Vectara.
With this bot you can create a Slack or Discord bot that is connected to your server and answers user questions by querying a Vectara corpus.

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

3. **Set Up Environment Variables:**
   - Create a `.env` file in the root of your project and add the following:
   ```
   SLACK_BOT_TOKEN=<OAuth level token>
   SLACK_APP_TOKEN=<APP level token>
   DISCORD_BOT_TOKEN=<Discord bot token>
   VECTARA_CUSTOMER_ID="<VECTARA_CUSTOMER_ID>"
   VECTARA_CORPUS_IDS="<VECTARA_CORPUS_IDS>"
   VECTARA_API_KEY="<VECTARA_API_KEY>"
   ACCOUNT_SID=<Twilio account SID>
   Auth_TOKEN=<Twilio auth token>
   TWILIO_WHATSAPP_NUMBER=<Whatsapp number configured in twilio>
   ```
   #### To enable [agentic rag](https://github.com/vectara/py-vectara-agentic) add the following variables.
   ```
   ENABLE_AGENTIC_RAG=True ## To enable agentic rag. By default ragtime uses vanilla RAG.
   AGENTIC_RAG_DATA_DESCRIPTION='Vectara website, docs and forum data'
   AGENTIC_RAG_ASSISTANT_SPECIALTY='Vectara'
   AGENTIC_RAG_TOOL_NAME='ask_vectara'
   ```
   - The `VECTARA_CUSTOMER_ID` and `VECTARA_CORPUS_IDS` point to your Vectara account and relevant corpora to use. 
   - `VECTARA_CORPUS_IDS` can be a single corpus ID (numeric) or a comma-separated list of corpora.
   
## Running ragtime bots

RagTime supports [Slack bot](#Steps-to-create-slack-bot),  [Discord bot](#Steps-to-create-discord-bot) and [Whatsapp bot](). 
You can run one of these, or all. 

### How to Run It Locally
- #### Running both bots
   ```bash
   python3 main.py
   ```
  
- #### Running only Slack bot
   ```bash
   python3 main.py slack
   ```

- #### Running only Discord bot
   ```bash
   python3 main.py discord
   ```
  
- #### Running only WhatsApp bot
   ```bash
   python3 main.py whatsapp
   ```  

### Run the application using Docker
**Build and Run with docker.**
- #### Running both bots
   ```bash
   bash run_docker.sh
   ```
- #### Running only Slack bot
   ```bash
   bash run_docker.sh slack
   ``` 
 - #### Running only Discord bot
   ```bash
   bash run_docker.sh discord
   ```
 - #### Running only Whatsapp bot
   ```bash
   bash run_docker.sh whatsapp
   ```   

## Steps to create Slack bot
In orer to connect your ragtime bot to your Slack service, follow these steps:

- Log in to your Slack workspace and navigate to the Slack API website. Click on "Your Apps" and then "Create New App." Provide a name for your app, select the workspace where you want to install it, and click "Create App."
- In the app settings, you can configure various details such as the app name, icon, and description. Make sure to fill out the necessary information accurately.
- Once you've configured your app, navigate to the "Install App" section. Click on the "Install App to Workspace" button to add the bot to your Slack workspace. This step will generate an OAuth access token that you'll need to use to authenticate your bot.
- To add user token scope, navigate to the "OAuth & Permissions" section in your app settings. Under the "OAuth Tokens for Your Workspace" section, you'll need to add  `app_mentions:read`, `channels:history`, `chat:write`, `chat:write.public`, `groups:history`, `im:history`, `mpim:history`, `mpim:read`, `mpim:write`, `users:read` scopes. Create the token and save it as `SLACK_BOT_TOKEN` in your `.env` file.
- Create an app level token with the `connection:write` scope. Save this token as `SLACK_APP_TOKEN` in your `.env` file.
- Make sure to save any changes you've made to your app settings and install/reinstall the bot to workplace.

## Steps to create Discord bot
In order to connect your ragtime bot to your Discord server, follow these steps:

- Navigate to [Discord Developer Portal Applications Page](https://discord.com/developers/applications) and create a new application by clicking on the ‘New Application‘ button on the top-right corner.
- Go to the ‘Bot‘ page by selecting the ‘Bot‘ option from the left column.
- Copy the provided token and save it as `DISCORD_BOT_TOKEN`.
- Choose ‘OAuth2’ from the left column and select the URL Generator.
- In the ‘Bot Permissions’ section at the bottom, select the necessary permissions.
- Choose the ‘bot’ option in the ‘Scope’ box, and the ‘BOT PERMISSIONS’ box will appear below it.
- Select ‘Read Message’, ‘Send Message’, and ‘Manage Message’ options.
- Copy the generated URL and paste it into your web browser. It will redirect you to the Discord page to add the bot to your server.


## How to setup whatsapp bot using twilio
In order to connect your ragtime whatsapp bot, follow these steps:

- Sign in to your [twilio console](https://console.twilio.com/).
- Navigate to the WhatsApp sandbox.
- Configure the `/whatsapp` endpoint for communication.
- Copy the Account SID, Auth Token, and WhatsApp Sandbox Number into `.env`

## Author

👤 **Vectara**

- Website: https://vectara.com
- Twitter: [@vectara](https://twitter.com/vectara)
- GitHub: [@vectara](https://github.com/vectara)
- LinkedIn: [@vectara](https://www.linkedin.com/company/vectara/)
- Discord: [@vectara](https://discord.gg/GFb8gMz6UH)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br/>
Feel free to check [issues page](https://github.com/vectara/ragtime/issues). You can also take a look at the [contributing guide](https://github.com/vectara/vectara-answer/blob/master/CONTRIBUTING.md).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2024 [Vectara](https://github.com/vectara).<br />
This project is [Apache 2.0](https://github.com/vectara/ragtime/blob/main/LICENSE) licensed.