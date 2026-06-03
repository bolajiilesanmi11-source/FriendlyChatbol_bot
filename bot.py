import os
import random
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

friendly_questions = [
    "How has your day been so far?",
    "What's something interesting that happened today?",
    "Do you have a favorite hobby?",
    "What's your favorite movie?",
    "If you could travel anywhere, where would you go?",
    "What are you currently learning?"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I'm Friendly Chat.\n\n"
        "Start a friendly conversation, ask questions, and chat anytime.\n\n"
        "How are you today?"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    if "hello" in user_text or "hi" in user_text:
        reply = "Hello! 😊 Nice to meet you. How's your day going?"
    elif "fine" in user_text or "good" in user_text:
        reply = random.choice(friendly_questions)
    elif "bye" in user_text:
        reply = "Goodbye! Have a wonderful day. 🌟"
    else:
        reply = random.choice(friendly_questions)

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()

if __name__ == "__main__":
    main()
