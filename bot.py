import os

import torch
import telebot
from telebot.types import InputMediaDocument
import openai

from processing.processor import Processor
from util.youtube import get_youtube_video_id


def set_seed(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


set_seed(1212)


openai.organization = os.getenv('OPENAI_ORG')
openai.api_key = os.getenv('OPENAI_API_KEY')
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'), num_threads=10)


@bot.message_handler(commands=['youtube'], content_types=['text'])
def send_youtube_video(message):
    youtube_link = message.text.split()[1]
    youtube_video_id = get_youtube_video_id(youtube_link)
    print(youtube_video_id)
    report_file = Processor.process_youtube_video(youtube_link, youtube_video_id)
    with open(report_file.full_path(), 'rb') as f:
        bot.send_media_group(
            message.from_user.id,
            [
                InputMediaDocument(f)
            ],
            reply_to_message_id=message.message_id
        )


if __name__ == '__main__':
    bot.infinity_polling()
