import asyncio
import importlib
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Dictionary mapping bot names to their respective module paths
BOT_MODULES = {
    "slack": "slack_bot",
    "discord": "discord_bot",
    "whatsapp": "whatsapp_bot"
}


async def start_bot(bot_name):
    """Dynamically imports and starts the specified bot."""
    module_name = BOT_MODULES.get(bot_name)
    if not module_name:
        raise ValueError(f"Invalid bot name: {bot_name}. Use 'slack', 'discord', or 'whatsapp'.")

    # Dynamically import the module and get the start function
    bot_module = importlib.import_module(module_name)
    start_function = getattr(bot_module, f"start_{bot_name}_bot")

    # Call the start function
    await start_function()


async def main(run_bot):
    if run_bot is None:
        # Run all bots based on environment settings
        bots_to_run = ["slack", "discord"]
        if os.getenv("TWILIO_WHATSAPP_NUMBER"):
            bots_to_run.append("whatsapp")
        await asyncio.gather(*(start_bot(bot) for bot in bots_to_run))
    else:
        # Run the specified bot
        await start_bot(run_bot.lower())


if __name__ == "__main__":
    run_bot = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(main(run_bot))
