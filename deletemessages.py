import asyncio

async def delete_message_later(message, delay=300):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")
