import os
import asyncio
import requests
import time
from flask import Flask, request, send_file
from threading import Thread
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler, 
    ConversationHandler, CallbackContext, filters
)
from addmovie import (
    start_add_movie, movie_name_handler, file_id_handler, 
    file_size_handler, file_name_handler, cancel, 
    MOVIE_NAME, FILE_ID, FILE_SIZE, FILE_NAME
)
from removemovie import remove_movie_command
from getfile import file_info
from listmovies import list_movies
from help import help_command
from movierequest import handle_movie_request
from sendmovie import send_movie
from filters import register_filters  # Import filters for link banning & auto-delete

# Fetch bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = "https://movie-master-68nu.onrender.com/webhook"  # Replace with your Render app URL

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable is missing! Set it before running the script.")

# Flask app for handling webhooks
app = Flask(__name__)

@app.route("/")
def home():
    return send_file("index.html")  # Serve index.html directly

@app.route("/webhook", methods=["POST"])
async def webhook():
    """Receive and process Telegram updates via webhook."""
    update = Update.de_json(request.get_json(), bot)
    await application.process_update(update)
    return "OK", 200

async def set_webhook():
    """Set the webhook for Telegram bot."""
    bot = Application.builder().token(BOT_TOKEN).build().bot
    await bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook set at {WEBHOOK_URL}")

def run_flask():
    """Run Flask app for webhook handling."""
    app.run(host="0.0.0.0", port=8080)

# Keep-alive function to prevent Render from sleeping
def keep_alive():
    url = "https://movie-master-68nu.onrender.com"  # Replace with your Render app URL
    while True:
        try:
            response = requests.get(url)
            print(f"✅ Keep-alive ping sent! Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Keep-alive request failed: {e}")
        time.sleep(49)  # Ping every 49 seconds

async def main():
    """Initialize bot, set webhook, and run Flask."""
    global application

    # Create Telegram bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register filters (Ban Links & Auto-Delete Messages)
    register_filters(application)

    # Command Handlers
    application.add_handler(CommandHandler("start", help_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, file_info))
    application.add_handler(CommandHandler("removemovie", remove_movie_command))
    application.add_handler(CommandHandler("listmovies", list_movies))

    # Conversation Handler for adding movies step by step
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler("addmovie", start_add_movie)],
        states={
            MOVIE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, movie_name_handler)],
            FILE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, file_id_handler)],
            FILE_SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, file_size_handler)],
            FILE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, file_name_handler)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    ))

    # Message Handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie_request))
    application.add_handler(CallbackQueryHandler(send_movie))

    # Set webhook
    await set_webhook()

    print("✅ Bot is running via webhook...")

if __name__ == "__main__":
    # Start Flask server in a separate thread
    Thread(target=run_flask, daemon=True).start()

    # Start keep-alive thread
    Thread(target=keep_alive, daemon=True).start()

    # Start bot asynchronously
    asyncio.run(main())
