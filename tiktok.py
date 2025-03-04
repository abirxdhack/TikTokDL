import os
import yt_dlp
import time
import logging
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize Pyrogram bot
app = Client("TikTokDownloaderBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to download TikTok video
def download_tiktok(url):
    output_filename = "tiktok_video.mp4"
    ydl_opts = {
        "format": "mp4",
        "outtmpl": output_filename,
        "quiet": False,  # Set to False to show logs for debugging
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Downloading TikTok video from: {url}")
            ydl.download([url])
        logger.info(f"Video downloaded successfully to: {output_filename}")
    except Exception as e:
        logger.error(f"Error downloading TikTok video: {e}")
        raise
    return output_filename

# Function to get video metadata
def get_video_metadata(url):
    ydl_opts = {
        'quiet': False,  # Enable logging for debugging
        'extract_flat': False,  # Ensure we get detailed information
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
            logger.info(f"Extracted info: {info_dict}")
            title = info_dict.get('title', 'N/A')
            views = info_dict.get('view_count', 0)
            duration = info_dict.get('duration', 0)
            return title, views, duration
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            return 'N/A', 0, 0

# Progress bar function for uploads
async def progress_bar(current, total, status_message: Message, start_time, last_update_time):
    elapsed_time = time.time() - start_time
    percentage = (current / total) * 100
    progress = "▓" * int(percentage // 5) + "░" * (20 - int(percentage // 5))
    speed = current / elapsed_time / 1024 / 1024  # Speed in MB/s
    uploaded = current / 1024 / 1024  # Uploaded size in MB
    total_size = total / 1024 / 1024  # Total size in MB

    # Throttle updates: Only update if at least 1 second has passed since the last update
    if time.time() - last_update_time[0] < 1:
        return
    last_update_time[0] = time.time()  # Update the last update time

    text = (
        f"📥 Upload Progress 📥\n\n"
        f"{progress}\n\n"
        f"🚧 Percentage: {percentage:.2f}%\n"
        f"⚡️ Speed: {speed:.2f} MB/s\n"
        f"📶 Uploaded: {uploaded:.2f} MB of {total_size:.2f} MB"
    )
    try:
        await status_message.edit(text)
    except Exception as e:
        logger.error(f"Error updating progress: {e}")

# Handler for /tt command
@app.on_message(filters.command("tt") & filters.private)
async def tiktok_handler(client, message):
    if len(message.command) < 2:
        await message.reply_text(
            "**❌ Please provide a TikTok video link.**",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    url = message.command[1]

    # Step 1: Send the initial "Searching Video" message
    status_message = await message.reply_text(
        "**Searching Video...**",
        parse_mode=ParseMode.MARKDOWN
    )

    try:
        # Step 2: Scrape video metadata (title, views, duration)
        title, views, duration = get_video_metadata(url)

        # Step 3: Download the TikTok video
        video_path = download_tiktok(url)

        # Step 4: Get user information
        if message.from_user:
            user_full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
            user_info = f"[{user_full_name}](tg://user?id={message.from_user.id})"
        else:
            group_name = message.chat.title or "this group"
            group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "this group"
            user_info = f"[{group_name}]({group_url})"

        # Convert duration to minutes and seconds
        duration_minutes = int(duration // 60)
        duration_seconds = int(duration % 60)

        # Step 5: Create the formatted message with scraped data
        caption = (
            f"🎵 **Title**: **{title}**\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"👁️‍🗨️ **Views**: **{views} views**\n"
            f"🔗 **Url**: [Watch On TikTok]({url})\n"
            f"⏱️ **Duration**: **{duration_minutes}:{duration_seconds:02d}**\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"**Downloaded By**: {user_info}"
        )

        # Step 6: Edit the message to show download details
        await status_message.edit(
            "**Found ☑️ Downloading...**",
            parse_mode=ParseMode.MARKDOWN
        )

        # Step 7: Start uploading the video with progress
        start_time = time.time()
        last_update_time = [start_time]  # Store the last update time to throttle the progress updates

        # Directly show the upload progress instead of "Found ☑️ Downloading..."
        await message.reply_video(
            video=video_path,
            caption=caption,
            progress=progress_bar,
            progress_args=(status_message, start_time, last_update_time)
        )

        # Step 8: Delete progress bar message after upload
        await status_message.delete()

        # Clean up the downloaded video file after sending
        os.remove(video_path)
        logger.info(f"Deleted the video file: {video_path}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        # If something goes wrong during the download, show error message
        await status_message.edit(
            "**❌ An Error Occurred**",
            parse_mode=ParseMode.MARKDOWN
        )

# Start the bot
if __name__ == "__main__":
    print("🚀 Bot is running...")
    app.run()
