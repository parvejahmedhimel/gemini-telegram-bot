import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- CONFIG --- #
BOT_TOKEN = "7490541464:AAF1K0BwkWUelTEZ7sOTMNIag8N4kHLAvyg"
GEMINI_API_KEY = "AIzaSyCuWpy2puh94gZa4A6STqrqsgFsRCzH7ko"
# --------------- #

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 হ্যালো! আমি Gemini AI বট। পড়াশোনায় সাহায্য লাগলে প্রশ্ন করো!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")

    try:
        response = model.generate_content(user_message)
        reply = response.text
    except Exception as e:
        reply = f"❌ কিছু ভুল হয়েছে: {e}"

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Gemini Bot চালু হয়েছে...")
    app.run_polling()

if __name__ == "__main__":
    main()
