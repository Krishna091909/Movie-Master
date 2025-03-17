from telegram import Update
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext):
    commands = """
    ✅ Available Commands:
    /start - Start the bot
    /fileinfo - Get file details
    /addmovie <movie_name> <file_id> <file_size> <file_name> - Add a movie
    /removemovie <movie_name> - Remove a movie
    /listmovies - Show all movies
    """
    await update.message.reply_text(commands)
