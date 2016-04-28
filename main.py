#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.

"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import telegram
import logging
import requests
from telegram import InlineQueryResultArticle, InputTextMessageContent

text_help = '''Welcome to AboutMovie!
This bot provides comprehensive movie info including reviews, ratings and biographies.
You can search your movie by "name", For example: X-Files
Or search by "name : year", for Example: X-Files : 1998'''

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text=text_help)


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text=text_help)


def echo(bot, update):
    name = ""
    year = ""
    if ":" in update.message.text:
        name = update.message.text.split(':')[0]
        year = update.message.text.split(':')[1]
    else:
        name = update.message.text

    print 'http://www.omdbapi.com/?t=' + name + '&y=' + year + '&plot=full&r=json'
    req = requests.get('http://www.omdbapi.com/?t=' + name + '&y=' + year + '&plot=full&r=json')

    if 'Error' in req.json():
        bot.sendMessage(update.message.chat_id,
                        '<b>Error: </b>' + req.json()['Error'],
                        parse_mode=telegram.ParseMode.HTML)
        return

    text = '<b>Title: </b>' + req.json()['Title'] + "\n" + \
           '<b>Year: </b>' + req.json()['Year'] + "\n" + \
           '<b>Released: </b>' + req.json()['Released'] + "\n" + \
           '<b>Genre: </b>' + req.json()['Genre'] + "\n" + \
           '<b>Director: </b>' + req.json()['Director'] + "\n" + \
           '<b>Writer: </b>' + req.json()['Writer'] + "\n" + \
           '<b>Actors: </b>' + req.json()['Actors'] + "\n" + \
           '<b>Country: </b>' + req.json()['Country'] + "\n" + \
           '<b>IMDb Rating: </b>' + req.json()['imdbRating'] + "\n" + \
           '<b>Plot: </b>' + req.json()['Plot'] + "\n" + \
           'http://www.imdb.com/title/' + req.json()['imdbID']

    bot.sendMessage(update.message.chat_id,
                    text,
                    photo=req.json()['Poster'],
                    parse_mode=telegram.ParseMode.HTML)


def inline_caps(bot, update):
    query = update.inline_query.query
    results = list()

    name = ""
    year = ""
    if ":" in update.inline_query.query:
        name = update.inline_query.query(':')[0]
        year = update.inline_query.query(':')[1]
    else:
        name = update.inline_query.query

    print 'http://www.omdbapi.com/?t=' + name + '&y=' + year + '&plot=full&r=json'
    req = requests.get('http://www.omdbapi.com/?t=' + name + '&y=' + year + '&plot=full&r=json')

    if 'Error' in req.json():
        bot.answerInlineQuery(update.inline_query.id, results)
        return

    text = '<b>Title: </b>' + req.json()['Title'] + "\n" + \
           '<b>Year: </b>' + req.json()['Year'] + "\n" + \
           '<b>Released: </b>' + req.json()['Released'] + "\n" + \
           '<b>Genre: </b>' + req.json()['Genre'] + "\n" + \
           '<b>Director: </b>' + req.json()['Director'] + "\n" + \
           '<b>Writer: </b>' + req.json()['Writer'] + "\n" + \
           '<b>Actors: </b>' + req.json()['Actors'] + "\n" + \
           '<b>Country: </b>' + req.json()['Country'] + "\n" + \
           '<b>IMDb Rating: </b>' + req.json()['imdbRating'] + "\n" + \
           '<b>Plot: </b>' + req.json()['Plot'] + "\n" + \
           'http://www.imdb.com/title/' + req.json()['imdbID']

    title = req.json()['Title'] + ", " + req.json()['Year'] + " by " + req.json()['Director']

    desc = req.json()['Plot']

    results.append(InlineQueryResultArticle(1,
                                            title=title,
                                            input_message_content=InputTextMessageContent(text,
                                                                                          parse_mode=telegram.ParseMode.HTML),
                                            description=desc,
                                            thumb_url=req.json()['Poster'],
                                            url='http://www.imdb.com/title/' + req.json()['imdbID']))

    bot.answerInlineQuery(update.inline_query.id, results)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("206673727:AAH7xvkKXCuPefYM5FqSX5qvbvqSL2Rldyc")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.addHandler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.addErrorHandler(error)

    inline_caps_handler = InlineQueryHandler(inline_caps)
    dp.addHandler(inline_caps_handler)
    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
