from loadmovies import remove_movie
from telegram import Update
from telegram.ext import CallbackContext

OWNER_ID = 7743703095  

async def remove_movie_command(update: Update, context: CallbackContext):
    # Check if the user is authorized
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    # Ensure a movie name is provided
    if not context.args:
        await update.message.reply_text("❌ Please provide a movie name to remove. Usage: /removemovie <movie_name>")
        return

    movie_name = " ".join(context.args)  # Combine all arguments into a single movie name
    if remove_movie(movie_name):  # Call the function that actually removes the movie
        await update.message.reply_text(f"🗑️ Movie '{movie_name}' removed successfully!")
    else:
        await update.message.reply_text("❌ Movie not found!")
