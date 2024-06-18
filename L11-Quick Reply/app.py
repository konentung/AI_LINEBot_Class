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
    TextMessage,
    QuickReply,
    QuickReplyItem,
    PostbackAction,
    MessageAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    PostbackEvent
)

app = Flask(__name__)

configuration = Configuration(access_token='gbd/MzpcTlmY5vChdTnVWYu9xxNHXQtJ6zVJTrd+32Gc2QXazt6oFUrCiO1XiQdEXsSIBzMOfYiH2liSVOSMBahGhi0K3EPmOD9GSHW6gU0pAdBFhYjYNe6WyrPzrW78rpFx+gSTBBznYTz/9ygNCwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('355fb806f8cb26d763ff9c2174b1f7bb')


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

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if text == 'quick_reply':
            postback_icon = request.url_root + 'static/postback.png'
            postback_icon = postback_icon.replace("http", "https")
            message_icon = request.url_root + 'static/message.png'
            message_icon = message_icon.replace("http", "https")
            datetime_icon = request.url_root + 'static/calendar.png'
            datetime_icon = datetime_icon.replace("http", "https")
            date_icon = request.url_root + 'static/calendar.png'
            date_icon = date_icon.replace("http", "https")
            time_icon = request.url_root + 'static/time.png'
            time_icon = time_icon.replace("http", "https")

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text='請選擇項目',
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyItem(
                                    action=PostbackAction(
                                        label="Postback",
                                        data="postback",
                                        display_text="postback"
                                    ),
                                    image_url=postback_icon
                                ),
                                QuickReplyItem(
                                    action=MessageAction(
                                        label="Message",
                                        text="message"
                                    ),
                                    image_url=message_icon
                                ),
                                QuickReplyItem(
                                    action=DatetimePickerAction(
                                        label="Date Picker",
                                        data="datetimepicker",
                                        mode="date"
                                    ),
                                    image_url=date_icon
                                ),
                                # QuickReplyItem(
                                #     action=DatetimePickerAction(
                                #         label="Time Picker",
                                #         data="datetimepicker",
                                #         mode="time"
                                #     ),
                                #     image_url=time_icon
                                # ),
                                # QuickReplyItem(
                                #     action=DatetimePickerAction(
                                #         label="Datetime Picker",
                                #         data="datetimepicker",
                                #         mode="datetime",
                                #         initial="2024-01-01T00:00",
                                #         max="2025-01-01T00:00",
                                #         min="2023-01-01T00:00"
                                #     ),
                                #     image_url=datetime_icon
                                # ),
                                # QuickReplyItem(
                                #     action=CameraAction(label="Camera")
                                # ),
                                # QuickReplyItem(
                                #     action=CameraRollAction(label="Camera Roll")
                                # ),
                                # QuickReplyItem(
                                #     action=LocationAction(label="Location")
                                # )
                            ]
                        )
                    )]
                )
            )

if __name__ == "__main__":
    app.run()