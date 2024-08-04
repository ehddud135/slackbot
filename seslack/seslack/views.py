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
from customer.models import CustomerList, Managerlist, Packages
from seslack.blocks import block_builder, modal_builder

load_dotenv()

view_modal = modal_builder
view_block = block_builder

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
    print(request)
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
            # Check Payload 1
            # print(payload)
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
        # print(blocks)
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
    blocks = view_modal.customer_append_modal_block()
    modal_view = view_modal.create_modal_view_block(
        "고객사 등록", blocks, True, "append_customer"
    )
    ack()
    try:
        # Call the views.publish method using the WebClient passed to listeners
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


@app.view("append_customer")
def append_customer(ack, body, view, client):
    ack()
    # 모달에서 제출된 데이터 추출
    view_state = view["state"]["values"]

    customer_name = view_state["customer_name_input"]["customer_name_input"]["value"]
    manager_name = view_state["manager_name_input"]["manager_name_input"]["selected_option"]["value"]
    append_date = view_state["append_date"]["append_date"]["selected_date"]

    # 데이터베이스에 저장
    CustomerList.objects.create(customer_name=customer_name, manager_name=manager_name, append_date=append_date)

    # 사용자에게 메시지 전송
    user_id = body["user"]["id"]
    client.chat_postMessage(
        channel=user_id,
        text=f"Thank you, {customer_name}. Your name ({manager_name}) has been recorded!"
    )


@app.action("open_modal_customer_delete")
def open_modal_customer_delete(ack, body, client):
    # print(body)
    user_id = body['user']['id']
    blocks = view_modal.customer_delete_modal_block(user_id)
    modal_view = view_modal.create_modal_view_block(
        "고객사 삭제", blocks, True, "delete_customer"
    )
    ack()
    try:
        # Call the views.publish method using the WebClient passed to listeners
        result = client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )
        print(result)
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


@app.view("delete_customer")
def delete_customer(ack, body, view, client):
    ack()
    print(client)
    print(view)
    print(body)


@app.action("open_modal_package_append")
def open_modal_package_append(ack, body, client):
    ack()
    print(body)
    blocks = view_modal.append_package_name_modal_block()
    modal_view = view_modal.create_modal_view_block(
        "패키지 등록", blocks, True, "append_package"
    )
    try:
        # Call the views.publish method using the WebClient passed to listeners
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


@app.view("append_package")
def db_append_package(ack, view):
    ack()
    # 모달에서 제출된 데이터 추출
    view_state = view["state"]["values"]
    package_name = view_state["input_package_name"]["input_package_name"]["value"]
    customer_name = view_state["input_customer_name"]["input_customer_name"]["value"]
    append_date = view_state["append_date"]["append_date"]["selected_date"]
    license_expire_date = view_state["license_expire_date"]["license_expire_date"]["selected_date"]
    os_type = view_state["os_type"]["os_type"]["selected_option"]["value"]

    # 데이터베이스에 저장
    # CustomerList.objects.create(customer_name=customer_name, manager_name=manager_name, append_date=append_date)
    Packages.objects.create(
        customer_name=customer_name,
        package_name=package_name,
        append_date=append_date,
        license_expire_date=license_expire_date,
        os_type=os_type
    )


@app.action("open_modal_customer_list")
def open_modal_customer_list(ack, body, client):
    ack()
    blocks = view_modal.customer_list_modal_block()
    modal_view = view_modal.create_modal_view_block(
        "고객사 목록", blocks, False, "customer_list"
    )
    try:
        # Call the views.publish method using the WebClient passed to listeners
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


# SE 인원 추가 시 사용 하는 부분
"""
@app.action("open_modal_append_manager")
def open_modal_append_manager(ack, body, client):
    ack()
    blocks = view_modal.append_manager_modal_block()
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


@app.view("db_append_manager")
def db_append_manager(ack, body, client, view):
    ack()
    user_id = body["user"]["id"]

    # 모달에서 제출된 데이터 추출
    view_state = view["state"]["values"]
    manager_name = view_state["input_manager_name"]["input_manager_name"]["value"]
    append_date = view_state["append_date"]["append_date"]["selected_date"]

    # 데이터베이스에 저장
    Managerlist.objects.create(user_id=user_id, manager_name=manager_name, append_date=append_date)
"""
