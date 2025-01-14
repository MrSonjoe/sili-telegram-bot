#!/usr/bin/env python3

from datetime import time
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater
import dota_api
import json
import logging
import random
import os

# Environment variable
token = os.environ['bot_token']
chat_id = os.environ['chat_id']


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

punlines = {}
with open("../resources/punlines.json", 'r') as f:
    punlines = json.load(f)


def get_dota_matches(context: CallbackContext) -> None:
    messages = dota_api.api_crawl()
    logger.info(f"messages: {messages}")

    if messages:
        messages = '\n\n'.join(messages)
        context.bot.send_message(chat_id=chat_id,
                                 text=messages)


def poll(context: CallbackContext) -> None:
    logger.info(f"DODO")

    questions = [random.choice(punlines[0]["ja"]),
                 random.choice(punlines[0]["nein"])]

    context.bot.send_voice(chat_id=chat_id, voice=open(
        '../resources/lets_dota.mpeg', 'rb'))

    context.bot.send_poll(
        chat_id,
        "DoDo?",
        questions,
        is_anonymous=False,
        allows_multiple_answers=False,
    )


def crawl(update: Update, context: CallbackContext):
    if update.effective_chat.id == int(chat_id):
        get_dota_matches(context)


def dodo(update: Update, context: CallbackContext):
    if update.effective_chat.id == int(chat_id):
        poll(context)


def doubt(update: Update, context: CallbackContext):
    if update.effective_chat.id == int(chat_id) and "doubt" in update.message.text:
        context.bot.send_animation(
            chat_id=chat_id, animation=open('../resources/i_daut_it.gif', 'rb'))


def main():

    updater = Updater(token)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    dispatcher.add_handler(CommandHandler('dodo', dodo))
    dispatcher.add_handler(CommandHandler('crawl', crawl))
    dispatcher.add_handler(MessageHandler(
        Filters.text & (~Filters.command), doubt))

    job_queue.run_repeating(get_dota_matches, interval=600, first=10)
    job_queue.run_daily(poll, time(0, 0, 0), days=(3,))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
