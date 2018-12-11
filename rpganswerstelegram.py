import os
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import argparse
from configparser import SafeConfigParser
from flask import Flask, request
from botlogic import *
from telepot.loop import OrderedWebhook

def indent(level):
    indentation = ""

    for i in range(0, level):
        indentation += "-"

    return indentation

def sendData(msg, bot, response):
    if bot == None:
        return

   content_type, chat_type, chat_id = telepot.glance(msg)
   if isinstance(response, botresponse) == false:
       return

  text = response.header + "\n"

  for textLine in response.lines:
      if textLine.lineType== "normal":
          text += textLine.text + "\n"
      if textLine.lineType == "table":
          text += indent(textLine.indent) + "[" + textLine.text + "]" + "\n"
      if textLine.lineType == "attribute":
          text += indent(textLine.indent) + textLine.attribute + ": " + textLine.attributeValue + "\n"

  bot.sendMessage(chat_id, text)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

#def handle(msg):
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text' :
        response = processCommand(msg["text"])
    else:
        response = "error"

    sendData(msg, bot, response)

def on_inline_query(msg):
    pass

def on_chosen_inline_result(msg):
    pass

# Main starts here
token = str(os.environ["telegram_token"])
bot = telepot.Bot(token) # Bot is created from the telepot class
app = Flask(__name__)
URL = str(os.environ["telegram_url"])
webhook = OrderedWebhook(bot, {'chat': on_chat_message,
                               'callback_query': on_callback_query,
                               'inline_query': on_inline_query,
                               'chosen_inline_result': on_chosen_inline_result})

@app.route('/', methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'

if __name__ == '__main__':
    app.run()
    printf("Executed the run")
    
if __name__ != '__main__':
    try:
        bot.setWebhook(URL)
    # Sometimes it would raise this error, but webhook still set successfully.
    except telepot.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
