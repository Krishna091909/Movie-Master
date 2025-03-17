from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters
from loadmovies import save_movie

# Define conversation states
MOVIE_NAME, FILE_ID, FILE_SIZE, FILE_NAME = range(4)

OWNER_ID = 7743703095  # Your Telegram ID

async def start_add_movie(update: Update, context: CallbackContext):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return ConversationHandler.END

    await update.message.reply_text("🎬 Please enter the **Movie Name**:")
    return MOVIE_NAME

async def movie_name_handler(update: Update, context: CallbackContext):
    context.user_data["movie_name"] = update.message.text
    await update.message.reply_text("📂 Now, please enter the **File ID**:")
    return FILE_ID

async def file_id_handler(update: Update, context: CallbackContext):
    context.user_data["file_id"] = update.message.text
    await update.message.reply_text("📏 Now, please enter the **File Size** (e.g., 541.92MB):")
    return FILE_SIZE

async def file_size_handler(update: Update, context: CallbackContext):
    context.user_data["file_size"] = update.message.text
    await update.message.reply_text("📄 Finally, please enter the **File Name** (e.g., movie.mkv):")
    return FILE_NAME

async def file_name_handler(update: Update, context: CallbackContext):
    context.user_data["file_name"] = update.message.text

    # Save movie to Google Sheets
    save_movie(
        context.user_data["movie_name"],
        context.user_data["file_id"],
        context.user_data["file_size"],
        context.user_data["file_name"]
    )

    await update.message.reply_text(f"✅ Movie '{context.user_data['movie_name']}' added successfully!")
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    """Cancel the movie addition process."""
    await update.message.reply_text("❌ Movie addition cancelled.")
    return ConversationHandler.END

