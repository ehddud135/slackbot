import json
import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler
from slack_sdk.errors import SlackApiError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customer.models import Manager
from ..blocks import block_builder, manager_modal_builder

load_dotenv()

manager_modal = manager_modal_builder
view_modal = block_builder

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

SLACK_SIGNING_SECRET = os.getenv('SIGNING_SECRET')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

manager_app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

handler = SlackRequestHandler(manager_app)


@csrf_exempt
def manager_events(request):
    if request.method == 'POST':
        if request.content_type == 'application/x-www-form-urlencoded':
            payload = request.POST.get('payload')
            if payload:
                return handler.handle(request)
    return JsonResponse({'status': 'ok'})


# SE 인원 추가 시 사용 하는 부분
# """
@manager_app.action("open_modal_append_manager")
def open_modal_append_manager(ack, body, client):
    ack()
    # print(body)
    blocks = manager_modal.append_manager_modal_block()
    modal_view = view_modal.create_modal_view_block(
        "db_append_manager", blocks, True
    )
    try:
        # Call the views.publish method using the WebClient passed to listeners
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


@manager_app.view("db_append_manager")
def db_append_manager(ack, body, client, view):
    ack()
    print(body)
    user_id = body["user"]["id"]
    # 모달에서 제출된 데이터 추출
    view_state = view["state"]["values"]
    manager_name = view_state["input_manager_name"]["input_manager_name"]["value"]
    append_date = view_state["append_date"]["append_date"]["selected_date"]

    # 데이터베이스에 저장
    Manager.objects.create(
        user_id=user_id,
        name=manager_name,
        created_at=append_date
    )
# """
