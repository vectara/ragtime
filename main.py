import asyncio
import sys
from dotenv import load_dotenv

from discord_bot import start_discord_bot
from slack_bot import start_slack_bot

load_dotenv()


async def main(run_bot):
    if run_bot.lower() == "slack":
        await start_slack_bot()
    elif run_bot.lower() == "discord":
        await start_discord_bot()
    elif run_bot is None:
        await asyncio.gather(start_slack_bot(), start_discord_bot())
    else:
        raise ValueError("Invalid argument. Use 'slack', 'discord', or don't pass any argument to run both bots.")

if __name__ == "__main__":
    run_bot = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(main(run_bot))
