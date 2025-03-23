import asyncio
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Function to detect links
def contains_link(text: str) -> bool:
    return bool(re.search(r"https?://\S+|www\.\S+|\S+\.\S{2,}", text))

# Function to ban links (Delete message + Send warning)
async def ban_links(update: Update, context: CallbackContext):
    if update.message:
        await update.message.delete()
        await update.message.reply_text(f"{update.message.from_user.mention_html()}, Links are not allowed!", parse_mode="HTML")

# Function to auto-delete messages after 5 minutes
async def auto_delete(update: Update, context: CallbackContext):
    if update.message:
        message = update.message
        await asyncio.sleep(300)  # Wait for 5 minutes
        try:
            await message.delete()
        except Exception:
            pass  # Ignore if message was already deleted

# Function to register the filters in bot.py
def register_filters(application: Application):
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"https?://\S+|www\.\S+|\S+\.\S{2,}"), ban_links))
    application.add_handler(MessageHandler(filters.ALL, auto_delete))
