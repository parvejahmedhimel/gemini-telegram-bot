import os
from dotenv import load_dotenv
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from flask import Flask, request

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Ex: https://your-render-app.onrender.com/your_bot_path

# Gemini Config
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Flask app for webhook
app = Flask(__name__)

telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 হ্যালো! আমি Gemini AI Webhook বট!")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")

    try:
        response = model.generate_content(user_message)
        reply = response.text or "😕 দুঃখিত, কিছু বুঝতে পারিনি।"
    except Exception as e:
        reply = f"❌ সমস্যা হয়েছে: {e}"

    await update.message.reply_text(reply)

# Add handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Set Webhook route
@app.route(f"/webhook", methods=["POST"])
def webhook() -> str:
    telegram_app.update_queue.put(Update.de_json(request.get_json(force=True), telegram_app.bot))
    return "OK", 200

# Set webhook on startup
@app.before_first_request
def init_webhook():
    telegram_app.bot.set_webhook(url=WEBHOOK_URL)

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
