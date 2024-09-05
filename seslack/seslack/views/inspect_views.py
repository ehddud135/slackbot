import json
import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler
from slack_sdk.errors import SlackApiError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customer.models import Customer, Manager, Packages
from ..blocks import inspect_modal_builder, block_builder
from slack_sdk.web.client import WebClient

load_dotenv()

view_modal = block_builder
inspect_modal = inspect_modal_builder

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

SLACK_SIGNING_SECRET = os.getenv('SIGNING_SECRET')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

inspect_app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

handler = SlackRequestHandler(inspect_app)


@csrf_exempt
def inspect_events(request):
    if request.method == 'POST':
        if request.content_type == 'application/x-www-form-urlencoded':
            payload = request.POST.get('payload')
            if payload:
                return handler.handle(request)
    return JsonResponse({'status': 'ok'})


# -------------------------------------------------------------------------------------

@inspect_app.action("open_modal_inspect_schedule")
def open_modal_modify_inspect_schedule(ack, body, client: WebClient):
    blocks = inspect_modal.modify_inspect_schedule_modal_block()
    modal_view = view_modal.create_modal_view_block(
        "점검 일정 변경", blocks, True, "modify_inspect_schedule"
    )
    ack()
    # print(body)
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


@inspect_app.view("modify_inspect_schedule")
def modify_inspect_schedule(ack, body, view, client):
    ack()
    # print(body)

# -------------------------------------------------------------------------------------


@inspect_app.action("open_modal_inspect_report")
def open_modal_inspect_report(ack, body, client: WebClient):
    # print(body)
    user_id = body['user']['id']
    blocks = view_modal.customer_delete_modal_block(user_id)
    modal_view = view_modal.create_modal_view_block(
        "점검 내역", blocks, True, "inspect_detail"
    )
    ack()
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


@inspect_app.action("update_inspect_report")
def update_inspect_report(ack, body, client: WebClient):
    print("update modal called")
    ack()
    selected_option = body['actions'][0]['selected_option']['value']
    blocks = view_modal.update_customer_delelte_modal_block(selected_option)
    updated_view = view_modal.create_modal_view_block(
        "고객사 삭제", blocks, True, "delete_customer"
    )

    try:
        client.views_update(
            view_id=body["view"]["id"],
            view=updated_view,
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


@inspect_app.view("inspect_detail")
def delete_customer(ack, body, view, client):
    ack()
    # 모달에서 제출된 데이터 추출
    view_state = view["state"]["values"]


# -------------------------------------------------------------------------------------
