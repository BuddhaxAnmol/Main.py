import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Facebook profile link
FACEBOOK_PROFILE_LINK = 'https://www.facebook.com/your_profile_link'

# Function to handle the start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the Facebook Video Downloader Bot! Send me a Facebook video link and choose an option to download.")

# Function to handle messages
def download_facebook_video(update: Update, context: CallbackContext) -> None:
    video_url = update.message.text
    keyboard = [
        ["Download in HD", "Download in MP3"],
        ["Download in MP4", "Contact Owner"]
    ]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    update.message.reply_text("Choose an option:", reply_markup=reply_markup)
    context.user_data['video_url'] = video_url

# Function to handle option selection
def option_selected(update: Update, context: CallbackContext) -> None:
    option = update.message.text
    video_url = context.user_data.get('video_url')
    if option == "Download in HD":
        download_video(update, video_url, quality='hd')
    elif option == "Download in MP3":
        download_audio(update, video_url)
    elif option == "Download in MP4":
        download_video(update, video_url, quality='sd')
    elif option == "Contact Owner":
        update.message.reply_text(f"Contact the owner: {FACEBOOK_PROFILE_LINK}")

# Function to download video
def download_video(update: Update, video_url: str, quality: str = 'sd') -> None:
    download_url = f'https://fbdownloader.net/download/?url={video_url}&quality={quality}'
    response = requests.get(download_url)
    if response.status_code == 200:
        file_name = f"video.{quality}.mp4"
        with open(file_name, "wb") as f:
            f.write(response.content)
        update.message.reply_document(document=open(file_name, "rb"))
        os.remove(file_name)
    else:
        update.message.reply_text("Failed to download video. Please try again.")

# Function to download audio
def download_audio(update: Update, video_url: str) -> None:
    audio_url = f'https://fbdownloader.net/download/?url={video_url}&quality=audio'
    response = requests.get(audio_url)
    if response.status_code == 200:
        file_name = "audio.mp3"
        with open(file_name, "wb") as f:
            f.write(response.content)
        update.message.reply_document(document=open(file_name, "rb"))
        os.remove(file_name)
    else:
        update.message.reply_text("Failed to download audio. Please try again.")

def main() -> None:
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Registering handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_facebook_video))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Download in HD|Download in MP3|Download in MP4|Contact Owner)$'), option_selected))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
  
