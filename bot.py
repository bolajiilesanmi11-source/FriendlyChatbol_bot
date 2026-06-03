import os
import logging
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Setup Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. Friendly Bot Logic
FRIENDLY_QUESTIONS = [
    "How has your day been so far? 😊",
    "What's something good that happened to you today?",
    "If you could travel anywhere right now, where would you go? ✈️",
    "What's your favorite hobby to unwind with?",
    "Are you working on anything exciting lately?"
]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"Hi {user_name}! 👋 Welcome to Friendly Chat.\n\n"
        "I'm here to chat, listen, and ask questions anytime you need a friend. "
        "How are you feeling today?"
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    
    if any(word in user_text for word in ["hello", "hi", "hey"]):
        reply = "Hey there! Great to hear from you. "
    elif any(word in user_text for word in ["good", "great", "happy", "fine"]):
        reply = "I'm so glad to hear that! Always love a positive vibe. "
    elif any(word in user_text for word in ["bad", "sad", "tired", "stressed"]):
        reply = "I'm really sorry to hear that. Take it easy on yourself today. 🧸 "
    else:
        reply = "Thanks for sharing that with me! "

    follow_up = random.choice(FRIENDLY_QUESTIONS)
    await update.message.reply_text(f"{reply}{follow_up}")

# 3. Main Application Execution
def main():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        logger.error("No TELEGRAM_TOKEN found in environment variables!")
        return

    # Build and run the application purely on polling
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Starting Telegram Bot as a Background Worker...")
    application.run_polling()

if __name__ == '__main__':
    main()
