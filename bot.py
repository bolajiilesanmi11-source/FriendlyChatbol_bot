import os
import logging
import random
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Setup Logging (Crucial for debugging and preventing silent errors)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. Flask Web Server (To keep Render happy)
app = Flask('')

@app.route('/')
def home():
    return "Friendly Chat Bot is alive and running!"

def run_web_server():
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 3. Friendly Bot Logic
FRIENDLY_QUESTIONS = [
    "How has your day been so far? 😊",
    "What's something good that happened to you today?",
    "If you could travel anywhere right now, where would you go? ✈️",
    "What's your favorite hobby to unwind with?",
    "Are you working on anything exciting lately?"
]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggered when /start is typed."""
    user_name = update.effective_user.first_name
    welcome_text = (
        f"Hi {user_name}! 👋 Welcome to Friendly Chat.\n\n"
        "I'm here to chat, listen, and ask questions anytime you need a friend. "
        "How are you feeling today?"
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming text messages, replies politely, and asks a follow-up question."""
    user_text = update.message.text.lower()
    
    # Simple keyword checking for a natural flow
    if any(word in user_text for word in ["hello", "hi", "hey"]):
        reply = "Hey there! Great to hear from you. "
    elif any(word in user_text for word in ["good", "great", "happy", "fine"]):
        reply = "I'm so glad to hear that! Always love a positive vibe. "
    elif any(word in user_text for word in ["bad", "sad", "tired", "stressed"]):
        reply = "I'm really sorry to hear that. Take it easy on yourself today. 🧸 "
    else:
        reply = "Thanks for sharing that with me! "

    # Add a random friendly question to keep the conversation going
    follow_up = random.choice(FRIENDLY_QUESTIONS)
    await update.message.reply_text(f"{reply}{follow_up}")

# 4. Main Application Initialization
def main():
    # Get token from environment variables (Best practice for security)
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        logger.error("No TELEGRAM_TOKEN found in environment variables!")
        return

    # Start the Flask server in a separate thread so it doesn't block the bot
    Thread(target=run_web_server).start()

    # Build the Telegram Bot application
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    logger.info("Starting Telegram Bot...")
    application.run_polling()

if __name__ == '__main__':
    main()
