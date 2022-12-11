
from __future__ import unicode_literals
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import QuickReply, QuickReplyButton, MessageAction

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

from init_kernal import InitKernal

kernal = InitKernal()

@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):

	if event.message.text in {'$', '＄'}:

		quick_reply = QuickReply(items=[
			QuickReplyButton(action=MessageAction(label="help", text="$ help")),
			QuickReplyButton(action=MessageAction(label="mod", text="$ mod")),
			QuickReplyButton(action=MessageAction(label="ls", text="$ ls")),
			QuickReplyButton(action=MessageAction(label="rels", text="$ rels")),
			QuickReplyButton(action=MessageAction(label="uid", text="$ uid")),
			QuickReplyButton(action=MessageAction(label="hello", text="$ hello")),
			QuickReplyButton(action=MessageAction(label="upload", text="$ upload")),
			QuickReplyButton(action=MessageAction(label="download", text="$ download")),
		])

		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(
				text='請選擇指令',
				quick_reply=quick_reply
			)
		)
		return

	(is_cmd, return_txt) = kernal.run(event)

	if not is_cmd: return

	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=return_txt)
	)

if __name__ == "__main__":
	app.run()


