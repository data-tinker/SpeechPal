from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import torch

import os

from processing.processor import Processor

BOT_TOKEN = os.environ.get('BOT_TOKEN')


def set_seed(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


set_seed(1212)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    youtube_link = 'https://www.youtube.com/watch?v=pQnOBHNKlgs'

    app.add_handler(CommandHandler("hello", Processor.process_youtube_link(youtube_link)))

    app.run_polling()