import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

from discord_bot import start_discord_bot
from slack_bot import start_slack_bot
from whatsapp_bot import start_whatsapp_bot

load_dotenv()


async def main(run_bot):
    if run_bot is None:
        if os.getenv("TWILIO_WHATSAPP_NUMBER"):
            await asyncio.gather(start_slack_bot(), start_discord_bot(), start_whatsapp_bot())
        else:
            await asyncio.gather(start_slack_bot(), start_discord_bot())
    elif run_bot.lower() == "slack":
        await start_slack_bot()
    elif run_bot.lower() == "discord":
        await start_discord_bot()
    elif run_bot.lower() == "whatsapp":
        await start_whatsapp_bot()
    else:
        raise ValueError("Invalid argument. Use 'slack', 'discord', or don't pass any argument to run both bots.")


if __name__ == "__main__":
    run_bot = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(main(run_bot))
