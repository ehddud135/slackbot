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
from .blocks import home_tab_blocks

load_dotenv()

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
        customer_db = CustomerList.objects.all()
        blocks = home_tab_blocks(customer_db)
        # Call the views.publish method using the WebClient passed to listeners
        result = client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "blocks": blocks
            },
        )
        # logger.debug("app_home_open result : %s", result)

    except SlackApiError as e:
        logger.error("Error fetching conversations: %s", e)


@app.action("approve_test")
def approve_test(ack, body, client):
    print("approve_test")
    ack()


@app.action("open_modal")
def open_modal(ack, body, client):
    # print(body)
    ack()
    try:
        # Call the views.publish method using the WebClient passed to listeners
        response = client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "callback_id": "append_customer",
                "title": {"type": "plain_text", "text": "고객사 등록", "emoji": True},
                "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
                "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
                "blocks": [
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": "고객사 등록 용", "emoji": True}
                    },
                    {
                        "type": "input",
                        "block_id": "customer_name_input",
                        "element": {"type": "plain_text_input", "action_id": "customer_name_input"},
                        "label": {"type": "plain_text", "text": "고객사명", "emoji": True}
                    },
                    {
                        "type": "input",
                        "block_id": "manager_name_input",
                        "element": {"type": "plain_text_input", "action_id": "manager_name_input"},
                        "label": {"type": "plain_text", "text": "담당자명", "emoji": True}
                    }
                ]
            },
        )
        # logger.debug("open_modal response %s", response)
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


@app.view("append_customer")
def append_customer(ack, body, view, client):
    ack()
    # 모달에서 제출된 데이터 추출
    customer_name = view["state"]["values"]["customer_name_input"]["customer_name_input"]["value"]
    manager_name = view["state"]["values"]["manager_name_input"]["manager_name_input"]["value"]

    # 데이터베이스에 저장
    CustomerList.objects.create(customer_name=customer_name, manager=manager_name)

    # 사용자에게 메시지 전송
    user_id = body["user"]["id"]
    client.chat_postMessage(
        channel=user_id,
        # text=f"Thank you, {customer_name}. Your age ({manager_name}) has been recorded!"
    )
