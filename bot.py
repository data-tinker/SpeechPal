import os
from collections import defaultdict

import openai
import telebot

from processing.processor import Processor

openai.organization = os.getenv('OPENAI_ORG')
openai.api_key = os.getenv('OPENAI_API_KEY')
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'), num_threads=10)

questions = [
    'Tell me about yourself',
    'Why do you want to work for our company?',
    'Tell me about a time when you started a project from scratch?',
    'Thank you for testing our bot! You can continue using it by recording an audio message or sending an audio file from your phone.',
]

user_questions = defaultdict(lambda: iter(questions))
users_in_testing_process = set()


@bot.message_handler(commands=['test'])
def process_test_question(message):
    user_id = message.from_user.id
    try:
        users_in_testing_process.add(user_id)
        next_question = next(user_questions[user_id])

        bot.send_message(user_id, next_question)
    except StopIteration:
        user_questions.pop(user_id)
        users_in_testing_process.remove(user_id)


@bot.message_handler(commands=['start'], content_types=['text'])
def process_youtube_video(message):
    bot.send_message(
        message.from_user.id,
        """
Enjoy using the SpeechPal Telegram bot to analyze your speech in audio and video formats, and improve your speaking skills with personalized recommendations.

To analyze your speech, you have multiple options:

🔵Audio message: simply upload it to the bot by sending the file or recording a new voice message within the chat.
🔵Audio on your phone: send the file to the bot by tapping on the paperclip icon in the chat and selecting the file.
🔵YouTube video: type /youtube and the video's link right afterward.

After you've provided the audio or video to the bot, it will process the content and analyze your speech. Once the analysis is complete, the bot will send you a detailed message with recommendations to help you improve your speech.
        """
    )


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
    if message.from_user.id in users_in_testing_process:
        process_test_question(message)


@bot.message_handler(content_types=['audio'])
def process_audio(message):
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    bot_create_response(
        message,
        Processor.process_telegram_audio(downloaded_file, file_info.file_unique_id, file_info.file_path)
    )


def bot_create_response(message, report_url):
    bot.send_message(
        message.from_user.id,
        report_url,
        reply_to_message_id=message.message_id
    )


if __name__ == '__main__':
    if not os.path.isdir("tmp"):
        os.mkdir('tmp')
    bot.infinity_polling()
