import datetime
import time
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import re
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

TOKEN_FILE='./token.txt'
LINKS_FILE='./links.txt'
LOG_FILE='./log.txt'
LINK_REGEX=r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
SONG_ANSWER="Sorry, I can't listen to that right now. I'm trying to finish this..."
VIDEO_ANSWER="Sorry, I can't watch that right now. I'm trying to finish this..."

with open(TOKEN_FILE) as f:
    TOKEN = f.readline()

LINKS = []
with open(LINKS_FILE) as f:
    for line in f:
        LINKS.append(line)

def print_log(message):
    print(message)
    with open(LOG_FILE, 'a+') as f:
        f.write(str(message) + '\n')

def start_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="YO!")

def select_link():
    return random.choice(LINKS)

def handle_link(update, context):
    if update.message != None and update.message.text != None:
        content = update.message.text
        if re.search('spotify',content):
            update.message.reply_text(SONG_ANSWER)
            updater.bot.send_message(update.effective_chat.id, select_link())
        elif re.search('youtu',content):
            update.message.reply_text(VIDEO_ANSWER)
            updater.bot.send_message(update.effective_chat.id, select_link())

def echo_and_print(update, context):
    print("RECEIVED!")
    print(datetime.datetime.now())
    print(update.message.text)

updater = Updater(TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.text, echo_and_print), 0)
updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(LINK_REGEX, re.IGNORECASE)), handle_link), 1)

updater.start_polling()
updater.idle()