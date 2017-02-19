from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
import logging
import config
import drugs_db
import csv
from datetime import datetime

telegram_token = config.telegram_token
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)

updater = Updater(telegram_token)
dispatcher = updater.dispatcher

emoji = u'\U0001F47B'
alco = emoji+'Алкоголь'
emoji = u'\U0001F3C3'
amph = emoji+'Амфетамин'
emoji = u'\U0001F389'
gomk = emoji+'Бутират'
emoji = u'\U0001F451'
cocaine = emoji+'Кокаин'
emoji = u'\U0001F6B5'
lsd = emoji+'ЛСД'
emoji = u'\U0001F60D'
mdma = emoji+'МДМА'
emoji = u'\U0001F590'
friend_bad_trip = emoji+'У моего друга бэд трип'
emoji = u'\U0001F47D'
iam_bad_trip = emoji + 'У меня бэд трип'

keyboard = [[InlineKeyboardButton(alco, callback_data='alco')],
              [InlineKeyboardButton(amph, callback_data='amph')],
              [InlineKeyboardButton(gomk, callback_data='gomk')],
            [InlineKeyboardButton(cocaine, callback_data='cocaine')],
            [InlineKeyboardButton(lsd, callback_data='lsd')],
            [InlineKeyboardButton(mdma, callback_data='mdma')],
            [InlineKeyboardButton(friend_bad_trip, callback_data='fbt')],
            [InlineKeyboardButton(iam_bad_trip, callback_data='iambt')]
            ]

def start(bot, update):
    text = 'Пожалуйста, выберите, о чем вы хотите узнать больше:'
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(chat_id=update.message.chat_id, reply_markup=reply_markup, text=text)
    with open('logs.csv', 'a+') as csvfile:
        logswriter = csv.writer(csvfile, delimiter = '\t')
        log = [str(datetime.now()), 'start']
        logswriter.writerow(log)


def button(bot, update):
    query = update.callback_query
    drug = query.data
    keyboard_back = [[InlineKeyboardButton(" <<< ", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard_back)
    if drug == 'back':
        text = 'Пожалуйста, выберите, о чем вы хотите узнать больше:'
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup,message_id=query.message.message_id)
    elif drug not in ('fbt', 'iambt'):
        text = drugs_db.drug_db[drug]['info']
        photo = drugs_db.drug_db[drug]['photo']
        bot.sendPhoto(chat_id=query.message.chat.id, photo = photo)
        bot.sendMessage(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup,message_id=query.message.message_id, parse_mode='HTML')
        with open('logs.csv', 'a+') as csvfile:
            logswriter = csv.writer(csvfile, delimiter='\t')
            log = [str(datetime.now()), drug]
            logswriter.writerow(log)
    else:
        text = drugs_db.drug_db[drug]['info']
        bot.sendMessage(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup,
                        message_id=query.message.message_id, parse_mode='HTML')
        with open('logs.csv', 'a+') as csvfile:
            logswriter = csv.writer(csvfile, delimiter='\t')
            log = [str(datetime.now()), drug]
            logswriter.writerow(log)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(CallbackQueryHandler(button))


dispatcher.add_handler(start_handler)

if __name__ == '__main__':
    #updater.start_polling()
    updater.start_webhook(listen='127.0.0.1', port=5002, url_path=telegram_token)
    updater.bot.setWebhook(webhook_url='https://95.85.37.72/' + telegram_token, certificate=open('/home/deploy/it-volunteer-bot/cert.pem', 'rb'))

