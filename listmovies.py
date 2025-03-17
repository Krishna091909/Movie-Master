from telegram import Update
from telegram.ext import CallbackContext
from loadmovies import load_movies

OWNER_ID = 7743703095  

async def list_movies(update: Update, context: CallbackContext):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    movies = load_movies()
    if movies:
        movie_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(movies.keys())])
        await update.message.reply_text(f"📜 **Movies List:**\n\n{movie_list}")
    else:
        await update.message.reply_text("❌ No movies available.")
