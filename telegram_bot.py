#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import random, os, sys, re

from io import BytesIO
import logging, sys

from image_processing import generate_image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('¡Hola!')
    update.message.reply_text('Bienvenido a GourmetBot\n'
    +'Modo de uso:\n'
    +'Modo de uso:\n'
    +'Modo de uso:')



def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('I need somebody! :-P')

def gen_img(update: Update, context: CallbackContext) -> None:
    """Generate an image."""
    context.bot.send_photo(update['message']['chat_id'], open(generate_image(update.message.text)[1], 'rb'))


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    # Returns a random photo with the message provided
    context.bot.send_photo(update['message']['chat_id'], open(generate_image(update.message.text)[0], 'rb'))


def photo(update: Update, context: CallbackContext):

    file = context.bot.get_file(update.message.photo[2].file_id)
    f =  BytesIO(file.download_as_bytearray())
    
    # f is now a file object you can do something with
    # generate a random name for tmp and destroy at the end
    with open("images_raw/tmp", "wb") as file:
        file.write(f.getbuffer())
    

    # +update.message.photo[-1].file_id
    keyboard = [
        [
            InlineKeyboardButton("Foto normal", callback_data="1:"),
            InlineKeyboardButton("Foto retro", callback_data="2:"),
        ],
        [InlineKeyboardButton("¡Sorpresa!", callback_data="3:")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # TO-DO: change tmp filename with a random one and delete afterwards to avoid collisions
    context.bot.send_photo(update['message']['chat_id'], open(generate_image(update.message.caption, "tmp")[0], 'rb'))

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
 
 #   update.message.reply_text('FUERA')


    query.edit_message_text(text=f"Selected option: {query.data}")

 #   if query.data == 1:
 #       update.message.reply_text('NORMAL')
 #       context.bot.send_photo(update['message']['chat_id'], open(generate_image(update.message.caption, "tmp")[0], 'rb'))
 #   elif query.data == 2:
 #       update.message.reply_text('RETRO')
 #       context.bot.send_photo(update['message']['chat_id'], open(generate_image(update.message.caption, "tmp")[1], 'rb'))




def main(main_token):
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    updater = Updater(main_token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CallbackQueryHandler(button))

    photo_handler = MessageHandler(Filters.photo, photo)
    dispatcher.add_handler(photo_handler)


    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(sys.argv[1])
        main(sys.argv[1])
    print("Needed a token for the bot")