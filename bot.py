import os

import torch
import telebot
import openai

from processing.processor import Processor


def set_seed(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


set_seed(1212)

openai.organization = os.getenv('OPENAI_ORG')
openai.api_key = os.getenv('OPENAI_API_KEY')
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'), num_threads=10)


@bot.message_handler(commands=['youtube'], content_types=['text'])
def process_youtube_video(message):
    youtube_link = message.text.split()[1]
    bot_create_response(Processor.process_youtube_video(youtube_link), message)


@bot.message_handler(content_types=['voice'])
def process_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    bot_create_response(
        message,
        Processor.process_telegram_voice(downloaded_file, file_info.file_unique_id)
    )


@bot.message_handler(content_types=['audio'])
def process_audio(message):
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    bot_create_response(
        message,
        Processor.process_telegram_audio(downloaded_file, file_info.file_unique_id, file_info.file_path)
    )


def bot_create_response(message, report_file):
    with open(report_file.full_path(), 'r') as f:
        response = f.read()
        if response:
            bot.send_message(
                message.from_user.id,
                response,
                reply_to_message_id=message.message_id
            )
        else:
            bot.send_message(
                message.from_user.id,
                "No errors, good job!",
                reply_to_message_id=message.message_id
            )


if __name__ == '__main__':
    if not os.path.isdir("tmp"):
        os.mkdir('tmp')
    bot.infinity_polling()
