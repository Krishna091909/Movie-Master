import os
import asyncio
import requests
import time
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler, 
    ConversationHandler, CallbackContext, filters
)
from addmovie import start_add_movie, movie_name_handler, file_id_handler, file_size_handler, file_name_handler, cancel, MOVIE_NAME, FILE_ID, FILE_SIZE, FILE_NAME
from removemovie import remove_movie_command
from getfile import file_info
from listmovies import list_movies
from loadmovies import load_movies
from help import help_command
from deletemessages import delete_message_later
from movierequest import handle_movie_request
from sendmovie import send_movie

# Fetch bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable is missing! Set it before running the script.")

# Flask app for keeping the bot alive
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Bot Status</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #121212;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
            }
            .container {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .loader {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: conic-gradient(
                    red, yellow, lime, cyan, blue, magenta, red
                );
                animation: spin 1s linear infinite;
            }
            .text {
                font-size: 1.5em;
                margin-top: 20px;
                animation: pulse 1.5s infinite alternate;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            @keyframes pulse {
                0% { opacity: 0.5; }
                100% { opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="loader"></div>
            <h2 class="text">Bot is Running...</h2>
        </div>
    </body>
    </html>
    """

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Keep-alive function to prevent Render from sleeping
def keep_alive():
    while True:
        try:
            requests.get("https://movie-master-3wbl.onrender.com")  # Replace with your Render app URL
            print("✅ Keep-alive ping sent!")
        except Exception as e:
            print(f"❌ Keep-alive request failed: {e}")
        time.sleep(49)  # Ping every 10 minutes

def main():
    # Start Flask server in a separate thread
    app_thread = Thread(target=run_flask)
    app_thread.start()

    # Start keep-alive thread
    keep_alive_thread = Thread(target=keep_alive)
    keep_alive_thread.start()

    # Initialize Telegram bot application
    tg_app = Application.builder().token(BOT_TOKEN).build()

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
