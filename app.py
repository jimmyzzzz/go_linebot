
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# LINE 聊天機器人的基本資料

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

from cmd_to_root import cmds_portal

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    
	user_id=event.source.user_id
	cmd_str=event.message.text
	
	(is_cmd, return_txt)=cmds_portal(cmd_str)
	
	if is_cmd:
		return_txt=f'to {user_id}:\n'+return_txt
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=return_txt)
		)

if __name__ == "__main__":
    app.run()
    
    
