from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    PostbackEvent
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    QuickReply,
    QuickReplyItem,
    PostbackAction
)
#Azure Translation
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

handler = WebhookHandler(CHANNEL_SECRET)
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_messsage(event):
    text = event.message.text
    quick_reply_items=[
        QuickReplyItem(
            action=PostbackAction(
                label="英文",
                data=f"lang=en&text={text}",
                display_text="英文"
            )
        ),
        QuickReplyItem(
            action=PostbackAction(
                label="日文",
                data=f"lang=ja&text={text}",
                display_text="日文"
            )
        ),
        QuickReplyItem(
            action=PostbackAction(
                label="繁體中文",
                data=f"lang=zh-Hant&text={text}",
                display_text="繁體中文"
            )
        ),
        QuickReplyItem(
            action=PostbackAction(
                label="文言文",
                data=f"lang=lzh&text={text}",
                display_text="文言文"
            )
        ),
        QuickReplyItem(
            action=PostbackAction(
                label="法文",
                data=f"lang=fr&text={text}",
                display_text="法文"
            )
        ),
        QuickReplyItem(
            action=PostbackAction(
                label="德文",
                data=f"lang=de&text={text}",
                display_text="德文"
            )
        ),
        QuickReplyItem(
            action=PostbackAction(
                label="西班牙文",
                data=f"lang=es&text={text}",
                display_text="西班牙文"
            )
        ),
        QuickReplyItem(
            action=PostbackAction(
                label="韓文",
                data=f"lang=ko&text={text}",
                display_text="韓文"
            )
        ),
    ]
    reply_message(event, [TextMessage(
        text='Please select a language:',
        quick_reply=QuickReply(
            items=quick_reply_items
        )
    )])

@handler.add(PostbackEvent)
def handle_postback(event):
    postback_data = event.postback.data
    params = {}
    for param in postback_data.split("&"):
        key, value = param.split("=")
        params[key] = value
    user_input = params.get("text")
    language = params.get("lang")
    result = azure_translate(user_input, language)
    reply_message(event, [TextMessage(text=result if result else "No translation available")])

def reply_message(event, messages):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages
            )
        )
        
def azure_translate(user_input, to_language):
    if to_language == None:
        return "選擇想要翻譯的語言"
    else:
        apikey = os.getenv("API_KEY")
        endpoint = os.getenv("ENDPOINT")
        region = os.getenv("REGION")
        credential = AzureKeyCredential(apikey)
        text_translator = TextTranslationClient(credential=credential, endpoint=endpoint, region=region)
        
        try:
            response = text_translator.translate(body=[user_input], to_language=[to_language])
            translation = response[0] if response else None

            if translation:
                detected_language = translation.detected_language
                result = ''
                if detected_language:
                    print(
                        f"Detected languages of the input text: {detected_language.language} with score: {detected_language.score}."
                    )
                for translated_text in translation.translations:
                    result = f"翻譯出的語言是:'{translated_text.to}'\n翻譯出的結果: '{translated_text.text}'"
                return result

        except HttpResponseError as exception:
            if exception.error is not None:
                print(f"Error Code: {exception.error.code}")
                print(f"Message: {exception.error.message}")

if __name__ == "__main__":
    app.run()