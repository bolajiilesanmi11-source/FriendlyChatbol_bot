import os
import logging
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# A list of friendly conversation starters
PROMPTS = [
    "How has your day been so far?",
    "What's something nice that happened to you today?",
    "If you could travel anywhere right now, where would you go?",
    "What's your favorite way to unwind after a long day?",
    "Tell me about a hobby you've been loving lately!"
]

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name
    welcome_text = (
        f"Hi {user_name}! 😊 I'm your Friendly Chat bot.\n\n"
        "I'm here to start a friendly conversation, ask questions, and chat anytime you need a friend. "
        "How are you doing today?"
    )
    await update.message.reply_text(welcome_text)

# /ask command handler (forces a new question)
async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = random.choice(PROMPTS)
    await update.message.reply_text(question)

# Message handler for general chatting
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()
    
    # Simple, friendly keyword responses
    if any(word in user_message for word in ["hello", "hi", "hey"]):
        reply = "Hey there! Great to hear from you. What's on your mind?"
    elif any(word in user_message for word in ["good", "great", "happy"]):
        reply = "That makes me so happy to hear! Tell me more about it. 🎉"
    elif any(word in user_message for word in ["bad", "sad", "tired", "bored"]):
        reply = "I'm sorry you're feeling that way. 🫂 I'm here to listen if you want to vent, or we can talk about something completely different to distract you!"
    else:
        # Default friendly response that keeps the conversation going
        follow_up = random.choice(PROMPTS)
        reply = f"Thanks for sharing that with me! Tell me, {follow_up.lower()}"

    await update.message.reply_text(reply)

def main():
    # Get the token from environment variables (important for Render security)
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logger.error("No TELEGRAM_TOKEN found in environment variables!")
        return

    # Build the application
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ask", ask_question))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Start the Bot using polling (great for simple Render Background Workers)
    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
