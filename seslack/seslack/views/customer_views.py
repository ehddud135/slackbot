
import json
import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler
from slack_sdk.errors import SlackApiError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customer.models import Customer, Manager, InspectionSchedule
from seslack.blocks import customer_modal_builder, block_builder
from slack_sdk.web.client import WebClient


load_dotenv()

customer_modal = customer_modal_builder
view_modal = block_builder

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

SLACK_SIGNING_SECRET = os.getenv('SIGNING_SECRET')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

customer_app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

handler = SlackRequestHandler(customer_app)


@csrf_exempt
def customer_events(request):
    if request.method == 'POST':
        if request.content_type == 'application/x-www-form-urlencoded':
            payload = request.POST.get('payload')
            if payload:
                return handler.handle(request)
    return JsonResponse({'status': 'ok'})


@customer_app.action("open_modal_customer_append")
def open_modal_customer_append(ack, body, client: WebClient):
    # print(body)
    blocks = customer_modal.customer_append_modal_block()
    modal_view = view_modal.create_modal_view_block(
        "고객사 등록", blocks, True, "append_customer"
    )
    ack()
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


@customer_app.view("append_customer")
def append_customer(ack, body, view, client):
    ack()
    # 모달에서 제출된 데이터 추출
    view_state = view["state"]["values"]

    customer_name = view_state["customer_name_input"]["customer_name_input"]["value"]
    manager_name = view_state["manager_name_input"]["manager_name_input"]["selected_option"]["value"]
    append_date = view_state["append_date"]["append_date"]["selected_date"]

    manager = Manager.objects.get(name=manager_name)
    # 데이터베이스에 저장
    Customer.objects.create(
        name=customer_name,
        manager=manager,
        created_at=append_date
    )

    customer = Customer.objects.get(name=customer_name)

    InspectionSchedule.objects.create(
        name=customer
    )

    # # 사용자에게 메시지 전송
    # user_id = body["user"]["id"]
    # client.chat_postMessage(
    #     channel=user_id,
    #     text=f"Thank you, {customer_name}. Your name ({manager_name}) has been recorded!"
    # )


@customer_app.action("open_modal_customer_delete")
def open_modal_customer_delete(ack, body, client: WebClient):
    # print(body)
    user_id = body['user']['id']
    blocks = customer_modal.customer_delete_modal_block(user_id)
    modal_view = view_modal.create_modal_view_block(
        "고객사 삭제", blocks, True, "delete_customer"
    )
    ack()
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


@customer_app.action("update_modal_customer_delete")
def update_modal_customer_delete(ack, body, client: WebClient):
    print("update modal called")
    ack()
    # print(body)
    selected_option = body['actions'][0]['selected_option']['value']
    print(selected_option)
    blocks = customer_modal.customer_delete_modal_update_block(selected_option)
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


@customer_app.view("delete_customer")
def delete_customer(ack, body, view, client):
    ack()
    # 모달에서 제출된 데이터 추출
    view_state = view["state"]["values"]
    # print(view_state)
    customer_name = view_state["select_customer"]["select_customer"]["selected_option"]["value"]
    # print(customer_name)
    customer = Customer.objects.get(name=customer_name)
    customer.delete()
    # manager_name = view_state["manager_name_input"]["manager_name_input"]["selected_option"]["value"]


@customer_app.action("open_modal_customer_list")
def open_modal_customer_list(ack, body, client):
    ack()
    blocks = customer_modal.customer_list_modal_block()
    modal_view = view_modal.create_modal_view_block(
        "고객사 목록", blocks, False, "customer_list"
    )
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))
