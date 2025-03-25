from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from loadmovies import load_movies

async def handle_movie_request(update: Update, context: CallbackContext):
    movies = load_movies()
    movie_name = update.message.text.lower()
    matched_movies = [key for key in movies.keys() if movie_name in key.lower()]

    if matched_movies:
        keyboard = [
            [InlineKeyboardButton(f"{movies[name]['file_size']} | {movies[name]['file_name']}", callback_data=name)]
            for name in matched_movies
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🎥 Lights, Camera, Action! Choose Your Film\n\n\n🕒 Hurry! This message vanishes in 5 minutes!", reply_markup=reply_markup)
    else:
        await update.message.reply_text("❌ Movie not found! Please check the spelling.")
