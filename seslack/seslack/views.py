# views.py
import json
import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler
from slack_sdk.errors import SlackApiError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customer.models import CustomerList
from . import blocks

load_dotenv()

view_block = blocks

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

SLACK_SIGNING_SECRET = os.getenv('SIGNING_SECRET')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

handler = SlackRequestHandler(app)


@csrf_exempt
def slack_events(request):

    if request.method == 'POST':
        if request.content_type == 'application/json':
            payload = request.body.decode('utf-8')
            print("payload print", payload)
            data = json.loads(payload)
            if data.get('type') == 'url_verification':
                return JsonResponse({'challenge': data['challenge']})
            return handler.handle(request)
        elif request.content_type == 'application/x-www-form-urlencoded':
            payload = request.POST.get('payload')
            if payload:
                data = json.loads(payload)
                return handler.handle(request)
    return JsonResponse({'status': 'ok'})


@app.event("app_home_opened")
def app_home_opened(event, client):
    # print("event: ", event)

    try:
        blocks = view_block.home_tab_blocks()
        user_id = event["user"]
        # Call the views.publish method using the WebClient passed to listeners
        client.views_publish(
            user_id=user_id,
            view={
                "type": "home",
                "blocks": blocks
            },
        )
        print("user_id is ", user_id)

    except SlackApiError as e:
        logger.error("Error fetching conversations: %s", e)


@app.action("approve_test")
def approve_test(ack, body, client):
    print("approve_test")
    ack()


@app.action("open_modal_customer_append")
def open_modal_customer_append(ack, body, client):
    # print(body)
    blocks = view_block.customer_append_modal_block()
    ack()
    try:
        # Call the views.publish method using the WebClient passed to listeners
        client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "callback_id": "append_customer",
                "title": {"type": "plain_text", "text": "고객사 등록", "emoji": True},
                "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
                "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
                "blocks": blocks
            },
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


@app.view("append_customer")
def append_customer(ack, body, view, client):
    ack()
    # 모달에서 제출된 데이터 추출
    customer_name = view["state"]["values"]["customer_name_input"]["customer_name_input"]["value"]
    manager_name = view["state"]["values"]["manager_name_input"]["manager_name_input"]["value"]
    append_date = view["state"]["values"]["append_date"]["append_date"]["value"]

    # 데이터베이스에 저장
    CustomerList.objects.create(customer_name=customer_name, manager=manager_name, append_date=append_date)

    # 사용자에게 메시지 전송
    user_id = body["user"]["id"]
    client.chat_postMessage(
        channel=user_id,
        # text=f"Thank you, {customer_name}. Your age ({manager_name}) has been recorded!"
    )


@app.action("open_modal_customer_delete")
def open_modal_customer_delete(ack, body, client):
    # print(body)
    user_id = body['user']['id']
    blocks = view_block.customer_delete_modal_block(user_id)
    ack()
    try:
        # Call the views.publish method using the WebClient passed to listeners
        client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "callback_id": "append_customer",
                "title": {"type": "plain_text", "text": "고객사 등록", "emoji": True},
                "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
                "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
                "blocks": blocks
            },
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))
