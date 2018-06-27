#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from urllib import parse, request
import logging
import json



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

global HOST = 'XXXX'

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('''  ''')


def download(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(''' ''')



def echo(bot, update):
    """Echo the user message."""
    text = update.message.text
    length = len(text)

    #update.message.reply_text('user: %s, from: %s, ' % (update.effective_user.username,update.message.chat_id))
    #bot.send_message(chat_id=update.message.chat_id, text='自定义回复')

    if "query=" in text:
        list = text.split('=')
        ethAdd = list[1]
        bot.send_message(chat_id=update.message.chat_id, text = ethAdd)
        apikey = 'XXXX'
        url = 'https://api.etherscan.io/api?module=account&action=balance&address=%s&tag=latest&apikey=%s' % (ethAdd,apikey)
        #getRequest(url)
        #https://api.etherscan.io/api?module=account&action=balance&address=0x4001F4373Db4000A7fC73f71dF982Cc08223f338&tag=latest&apikey=JYE89T7K5XY5Z5FJ3XTQHFQQSXMZUWH5G3


        req = request.Request(url)

        bot.send_message(chat_id = update.message.chat_id, text ='req: %s' % (req))

        res = request.urlopen(req)
        res = res.read()
        res_data = json.loads(res.decode('utf-8'))
        result = res_data['result']
        status = res_data['status']

        if (status == '1'):
            result = float(result)
            result = result / 1000000000000000000.00000
            update.message.reply_text('ETH余额：%s' % (result))
        else:
            update.message.reply_text('查询错误,请输入正确格式地址')
        #bot.send_message(chat_id=update.message.chat_id, text='req: %s' % (res))


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def unknown(bot, update):

    text = update.message.text
    length = len(text)
    text = text.replace('/', '')
    if text.isalnum():
        if length == 7:
            groupId = update.message.chat_id
            userId = update.effective_user.username
            global HOST
            url = '%s?groupId=%s&userId=%s&invitationCode=%s' % (HOST,groupId, userId, text)
            req = request.Request(url)

            # bot.send_message(chat_id = update.message.chat_id, text ='req: %s' % (req))

            res = request.urlopen(req)
            res = res.read()
            res_data = json.loads(res.decode('utf-8'))
            data = res_data['data']

            result = data['result']
            error = data['error']
            # bot.send_message(chat_id=update.message.chat_id, text=res_data)

            if result == True:
                success_text = '''
                .
                .
                .
                '''

                update.message.reply_text('Received codes  \n%s' % (success_text))
            else:
                error_text = '绑定失败'
                if error == 1:
                    error_text = '绑定失败,邀请码不存在。 \n \n Binding failed,The invitation code does not exist.'
                elif error == 2:
                    error_text = '绑定失败,邀请码已被申请。 \n \n Binding failed,The invitation code has been used.'
                elif error == 3:
                    error_text = '绑定失败,您已绑定过申请码。 \n \n Binding failed,You have successfully bundled.'
                else:
                    error_text = '绑定失败'
                update.message.reply_text(error_text)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("XXXX")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("download", download))

    echo_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(echo_handler)

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(CommandHandler(Filters.text, commendecho))


    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

