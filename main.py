import telebot
import os
import requests
from pytube import YouTube
bot_token = '6247720685:AAHlexDju9pAkjVsGMcG7x1-DoC5Bwouv8o'
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me a link to the video you want to download.")


@bot.message_handler(func=lambda message: True)
def download_video(message):
    try:
        link = message.text
        video = YouTube(link)
        title = video.title
        stream = video.streams.get_by_resolution('720p')
        if stream is not None:
            filename = f"{title}.mp4"
            stream.download(filename=filename)
            bot.send_video(message.chat.id, open(filename, 'rb'), caption="Here's your video!\n"
                           f"Video name - {video.title}. \n"
                           f"Author video - {video.author}")
            os.remove(filename)
        else:
            bot.reply_to(message, "Sorry, I couldn't find a stream for the video.")
    except Exception as e:
        bot.reply_to(message, f"Sorry, I couldn't download the video. Error: {e}")

bot.polling()
