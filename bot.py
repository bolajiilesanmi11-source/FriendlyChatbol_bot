import os
import sys
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 1. Setup logging so we can see what's happening in the Render logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. This is the function that runs when someone types /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /start command from a user!")
    
    welcome_text = (
        "👋 Welcome to Friendly Chat!\n"
        "Start a friendly conversation, ask questions, and chat anytime.\n"
        "Have a great day! 😊"
    )
    
    await update.message.reply_text(welcome_text)

# 3. The main engine that boots up the bot
async def main():
    # Grab the token from Render's environment variables
    token = os.environ.get("BOT_TOKEN")
    
    if not token:
        logger.error("ERROR: BOT_TOKEN variable is missing in Render settings!")
        sys.exit(1)

    logger.info("Initializing bot application...")
    # Build the bot
    app = Application.builder().token(token).build()

    # Link the /start command to our function
    app.add_handler(CommandHandler("start", start_command))

    # Start listening to Telegram
    logger.info("Friendly Chat Bot is now ONLINE and listening for messages... 🎉")
    
    # This keeps the bot running forever in the background
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Keep running until Render stops the script
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    # This forces Python to run the async loop safely from the beginning
    asyncio.run(main())
