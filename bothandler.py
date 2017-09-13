# -*- coding: utf-8 -*-
import telebot
import constant
from sendmail import sendEmail



bot = telebot.TeleBot(constant.token)

templ = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start','/stop')
    user_markup.row('/send')
    bot.send_message(message.from_user.id, 'Welcome', reply_markup=user_markup)

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Goodbye', reply_markup=hide_markup)

@bot.message_handler(commands=['send'])
def handle_send(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, 'При отправке соблюдайте посследовательность логин, пароль, получатель, тема,текск')

@bot.message_handler(content_types=['text'])
def handle_login(message):
    login, passw, receiver, subject, text = message.text.split(',')
    templ['login'] = login.strip()
    templ['passw'] = passw.strip()
    templ['receiver'] = receiver.strip()
    templ['subject'] = subject.strip()
    templ['text'] = text.strip()
    sendEmail(templ['login'],templ['passw'],templ['receiver'],templ['subject'],templ['text'])
    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, 'Отправлено')
    templ.clear()


bot.polling(none_stop=True)