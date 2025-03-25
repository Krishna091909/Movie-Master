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
        await update.message.reply_text("\n🎥 𝗟𝗶𝗴𝗵𝘁𝘀, 𝗖𝗮𝗺𝗲𝗿𝗮, 𝗔𝗰𝘁𝗶𝗼𝗻! 𝗖𝗵𝗼𝗼𝘀𝗲 𝗬𝗼𝘂𝗿 𝗙𝗶𝗹𝗺\n🕒 𝗛𝘂𝗿𝗿𝘆! 𝗧𝗵𝗶𝘀 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘃𝗮𝗻𝗶𝘀𝗵𝗲𝘀 𝗶𝗻 𝟱 𝗺𝗶𝗻𝘂𝘁𝗲𝘀!\n", reply_markup=reply_markup)
    else:
        await update.message.reply_text("❌ Movie not found! Please check the spelling.")
