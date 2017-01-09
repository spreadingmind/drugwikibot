from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
import logging
import config
import drugs_db


telegram_token = config.telegram_token
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)

PORT = int(os.environ.get('PORT', '5000'))
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


keyboard = [[InlineKeyboardButton(alco, callback_data='alco')],
              [InlineKeyboardButton(amph, callback_data='amph')],
              [InlineKeyboardButton(gomk, callback_data='gomk')],
            [InlineKeyboardButton(cocaine, callback_data='cocaine')],
            [InlineKeyboardButton(lsd, callback_data='lsd')],
            [InlineKeyboardButton(mdma, callback_data='mdma')]
            ]

def start(bot, update):
    text = 'Пожалуйста, выберите, о чем вы хотите узнать больше:'
    reply_markup = InlineKeyboardMarkup(keyboard)
    #update.message.reply_text(text, reply_markup=reply_markup)
    print(update.message.chat_id)
    bot.sendMessage(chat_id=update.message.chat_id, reply_markup=reply_markup, text=text)
    text='start' + ' ' + str(update.message.chat_id)
    bot.sendMessage(chat_id=47303188, text = text)

def button(bot, update):
    query = update.callback_query
    drug = query.data
    keyboard_back = [[InlineKeyboardButton(" <<< ", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard_back)
    if drug == 'back':
        text = 'Пожалуйста, выберите, о чем вы хотите узнать больше:'
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup,message_id=query.message.message_id)

    else:
        text = drugs_db.drug_db[drug]['info']
        photo = drugs_db.drug_db[drug]['photo']

        bot.sendPhoto(chat_id=query.message.chat.id,photo = photo)
        bot.sendMessage(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup,message_id=query.message.message_id, parse_mode='HTML')
        text2 = drug + ' ' + query.message.chat.id
        bot.sendMessage(chat_id=47303188, text=text2)
        print(text2)


start_handler = CommandHandler('start', start)
updater.dispatcher.add_handler(CallbackQueryHandler(button))


dispatcher.add_handler(start_handler)

if __name__ == '__main__':
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=telegram_token)
    updater.bot.setWebhook("https://drug-wiki.herokuapp.com/" + telegram_token)
    updater.idle()
