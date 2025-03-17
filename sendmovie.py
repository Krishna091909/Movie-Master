import asyncio
from telegram import Update
from telegram.ext import CallbackContext
from loadmovies import load_movies
from deletemessages import delete_message_later

async def send_movie(update: Update, context: CallbackContext):
    query = update.callback_query
    user_message = query.message  # User's message (button click)
    await query.answer()

    movie_name = query.data
    movies = load_movies()
    movie_data = movies.get(movie_name)

    if movie_data:
        user_id = query.from_user.id  
        file_id = movie_data["file_id"]
        file_size = movie_data["file_size"]
        file_name = movie_data["file_name"]

        # Send movie file to user DM
        sent_message = await context.bot.send_document(
            chat_id=user_id, 
            document=file_id, 
            caption=f"🎬 *{file_name}*\n📦 *Size:* {file_size}",
            parse_mode="Markdown"
        )

        # Send confirmation message in group
        msg = await query.message.reply_text("📩 Check your DM for the movie file!")

        # Schedule deletion after 5 minutes (300 seconds)
        asyncio.create_task(delete_message_later(sent_message, 300))  # Delete bot message in DM
        asyncio.create_task(delete_message_later(msg, 300))  # Delete confirmation message
        asyncio.create_task(delete_message_later(user_message, 300))  # Delete user message (button click)

    else:
        error_msg = await query.message.reply_text("❌ Movie not found.")
        asyncio.create_task(delete_message_later(error_msg, 300))  # Delete error message
        asyncio.create_task(delete_message_later(user_message, 300))  # Delete user message (button click)
