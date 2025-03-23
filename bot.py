
import os
import asyncio
import requests
import time
from flask import Flask, send_file
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
from loadmovies import load_movies
from help import help_command
from movierequest import handle_movie_request
from sendmovie import send_movie
from filters import register_filters  # Import filters for link banning & auto-delete

# Fetch bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable is missing! Set it before running the script.")

# Flask app for keeping the bot alive
app = Flask(__name__)

@app.route('/')
def home():
    return send_file("index.html")  # Serve index.html directly

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Keep-alive function to prevent Render from sleeping
def keep_alive():
    url = "https://cinema-club.onrender.com"  # Replace with your Render app URL
    while True:
        try:
            response = requests.get(url)
            print(f"✅ Keep-alive ping sent! Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Keep-alive request failed: {e}")
        time.sleep(49)  # Ping every 49 seconds

def main():
    # Start Flask server in a separate thread
    Thread(target=run_flask, daemon=True).start()

    # Start keep-alive thread
    Thread(target=keep_alive, daemon=True).start()

    # Initialize Telegram bot application
    tg_app = Application.builder().token(BOT_TOKEN).build()

    # Register filters (Ban Links & Auto-Delete Messages)
    register_filters(tg_app)

    # Command Handlers
    tg_app.add_handler(CommandHandler("start", help_command))
    tg_app.add_handler(CommandHandler("help", help_command))
    tg_app.add_handler(MessageHandler(filters.Document.ALL, file_info))
    tg_app.add_handler(CommandHandler("removemovie", remove_movie_command))
    tg_app.add_handler(CommandHandler("listmovies", list_movies))

    # Conversation Handler for adding movies step by step
    tg_app.add_handler(ConversationHandler(
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
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie_request))
    tg_app.add_handler(CallbackQueryHandler(send_movie))

    print("✅ Bot is running...")
    tg_app.run_polling()

if __name__ == "__main__":
    main()
