from telegram import Update
from telegram.ext import CallbackContext

OWNER_ID = 7743703095  # Your Telegram ID

async def file_info(update: Update, context: CallbackContext):
    if not update.message:
        #print("DEBUG: No message received.")
        return

    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    document = update.message.document
    if not document:
        #print("DEBUG: No document received.")
        await update.message.reply_text("Please send a movie file.")
        return

    file_id = document.file_id
    file_size_bytes = document.file_size
    file_size_mb = file_size_bytes / (1024 * 1024)  # Convert bytes to MB
    file_name = document.file_name

    # Debug print to check values
    #print(f"DEBUG: File ID: {file_id}, Size: {file_size_mb:.2f}MB, Name: {file_name}")

    # Correct reply format
    response_text = f"🎬 *File Name:\n* `{file_name}`\n\n📦 *Size:\n* `{file_size_mb:.2f}MB`\n\n🆔 *File ID:\n* `{file_id}`"

    await update.message.reply_text(response_text, parse_mode="MarkdownV2")
