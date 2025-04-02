import asyncio
from telegram import Update
from telegram.ext import CallbackContext
from loadmovies import load_movies
from deletemessages import delete_message_later

FILMSTREAM_BOT_USERNAME = "@Cine_File_Downloader_bot"  # Replace with your actual Filestream bot username

async def send_movie(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    movie_name = query.data
    movies = load_movies()
    movie_data = movies.get(movie_name)

    if movie_data:
        user_id = query.from_user.id  
        file_id = movie_data["file_id"]
        file_size = movie_data["file_size"]
        file_name = movie_data["file_name"]

        # Send movie file in DM with Filestream bot username
        sent_message = await context.bot.send_document(
            chat_id=user_id, 
            document=file_id, 
            caption=f"🎬 *{file_name}*\n📦 *Size:* {file_size}\n\n🤖 Forward this to {FILMSTREAM_BOT_USERNAME} to get fast download & online streaming links.",
            parse_mode="Markdown"
        )

        # Get the message object containing movie selection buttons
        user_message = query.message  

        # Schedule deletion of movie selection buttons **AFTER 5 MINUTES**
        asyncio.create_task(delete_message_later(user_message, 300))  

        # Also delete the user's search message after 5 minutes
        search_message = context.user_data.get("last_search_message")
        if search_message:
            asyncio.create_task(delete_message_later(search_message, 300))
            context.user_data["last_search_message"] = None  # Clear stored message

    else:
        error_msg = await query.message.reply_text("❌ Movie not found.")
        await asyncio.sleep(5)  # Small delay before deletion
        asyncio.create_task(delete_message_later(error_msg, 300))  # Delete error message
