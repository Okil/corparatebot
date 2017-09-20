import  telebot
import sendmail
import time
import os
import constant
bot = telebot.TeleBot(constant.token)

templ = {'lg': '', 'pw': '', 'rec': '', 'sb': '', 'txt': ''}


def log(message):
    print('=='*10)
    print(' Time:' + str(time.ctime()),'\n First Name: ' + message.from_user.first_name, '\n Last Name: ' + message.from_user.last_name,
          '\n Id user: ' + str(message.from_user.id), '\n E-mail: ' + templ['lg'], '\n Reciver: ' + templ['rec'])

# Handle '/start' and '/help'
@bot.message_handler(commands=['send'])
def send_welcome(message)
    msg = bot.reply_to(message, """\
        Привет Я почта бот, чтоб отправить email \n ведите логин от webmail.infosystems.uz
    """)
    bot.register_next_step_handler(msg, process_login_step)


def process_login_step(message):
    try:
        templ['lg'] = message.text
        msg = bot.reply_to(message, 'Пароль')
        bot.register_next_step_handler(msg, process_passw_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_passw_step(message):
    try:
        templ['pw'] = message.text
        msg = bot.reply_to(message, 'Получатель')
        bot.register_next_step_handler(msg, process_rec_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_rec_step(message):
    try:
        templ['rec'] = message.text
        msg = bot.reply_to(message, 'Тема')
        bot.register_next_step_handler(msg, process_sub_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_sub_step(message):
    try:
        templ['sb'] = message.text
        msg = bot.reply_to(message, 'Text')
        bot.register_next_step_handler(msg, process_text_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_text_step(message):
    try:
        templ['text'] = message.text
        sendmail.sendEmail(templ['lg'], templ['pw'], templ['rec'], templ['sb'], templ['text'])
        bot.send_chat_action(message.fr_user.id, 'typing')
        bot.send_message(message.from_user.id, 'Ваше сообщения отправлено на {}'.format(templ['rec']))
        log(message)
        templ.clear()

    except Exception as e:
        bot.reply_to(message, 'ooooops')
        print(e)


try:
    if __name__ == '__main__':
        bot.polling()

except Exception as e:
    os.system('python3.5 bot.py')