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
    ImagemapArea,
    ImagemapBaseSize,
    ImagemapExternalLink,
    ImagemapMessage,
    ImagemapVideo,
    URIImagemapAction,
    MessageImagemapAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,

)

app = Flask(__name__)

configuration = Configuration(access_token='C0c4QgaeqsP2OB7tfpmorNJ0IOHsLmv50DEQhPIIIDdInlJ2kb3BQ669t+7bbI0Y/1Yy63OCScnuQLYupqvJI85/lGsdGNs+5tEY66fHYaAVGcV4nWgmzgDlP71UenmMLBPzBs/YEzaZHds5uy8ayQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('19116491baccb3c5b8f81124b4d28796')


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
        if text == 'imagemap':
            url1 = request.url_root + '/static/imagemap'
            url1 = url1.replace("http", "https")
            app.logger.info("url=" + url1)
            url2 = request.url_root + '/static/video.mp4'
            url2 = url2.replace("http", "https")
            app.logger.info("url=" + url2)
            url3 = request.url_root + '/static/preview_image.png'
            url3 = url3.replace("http", "https")
            app.logger.info("url=" + url3)
            imagemap_message = ImagemapMessage(
                base_url=url1,
                alt_text='this is an imagemap',
                base_size=ImagemapBaseSize(height=1040, width=1040),
                video=ImagemapVideo(
                    original_content_url=url2,
                    preview_image_url=url3,
                    area=ImagemapArea(
                        x=0, y=0, width=1040, height=520
                    ),
                    external_link=ImagemapExternalLink(
                        link_uri='https://www.youtube.com/@bigdatantue',
                        label='點我看更多',
                    ),
                ),
                actions=[
                    URIImagemapAction(
                        type = "uri",
                        linkUri='https://instagram.com/ntue.bigdata?igshid=YmMyMTA2M2Y=',
                        area=ImagemapArea(
                            x=0, y=520, width=520, height=520
                        )
                    ),
                    MessageImagemapAction(
                        type ="message",
                        text='這是fb網頁https://www.facebook.com/NTUEBIGDATAEDU',
                        area=ImagemapArea(
                            x=520, y=520, width=520, height=520
                        )
                    )
                ]
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[imagemap_message]
                )
            )

if __name__ == "__main__":
    app.run()