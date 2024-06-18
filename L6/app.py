from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,
    BroadcastRequest,
    MulticastRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='3pgf0RBSuWmhPr9Fwz5HridYTB7vU+Q0+7T7877LRia8jh8n3tNdzsDJ3wZxAaPb1px0fD0bOuS1jVTdzdRrcTnQo5W8YuMdeqKgSx0Htvy62d33nNHBqWLr5xEs/5Cz2akAMSjpaxJq1j9R0lPPTAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('974e569266e988233dab6503bbdd1960')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 訊息事件
@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        # Reply message

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text ='reply message')]
            )
        )

        # result = line_bot_api.reply_message_with_http_info(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[TextMessage(text = "reply message with http info")]
        #     )
        # )

        # Push message
        
        line_bot_api.push_message_with_http_info(
            PushMessageRequest(
                to=event.source.user_id,
                messages=[TextMessage(text='PUSH!')]
            )
        )

        # Broadcast message
        
        # line_bot_api.broadcast_with_http_info(
        #     BroadcastRequest(
        #         messages=[TextMessage(text='BROADCAST!')]
        #     )
        # )

        # Multicast message
        
        # line_bot_api.multicast_with_http_info(
        #     MulticastRequest(
        #         to=['U2523f12efc62a10443c93abb089a432f'],
        #         messages=[TextMessage(text='MULTICAST!')],
        #         notificationDisabled=True
        #     )
        # )
            
if __name__ == "__main__":
    app.run()