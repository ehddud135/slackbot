import json
import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler
from slack_sdk.errors import SlackApiError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customer.models import Packages, Customer
from ..blocks import package_modal_builder, block_builder
from slack_sdk.web.client import WebClient
from ..Utiliy import Utiliy
from ..blocks.DatabaseAccessor import DatabaseAccessor

util = Utiliy()
DA = DatabaseAccessor()

load_dotenv()

package_modal = package_modal_builder
view_modal = block_builder

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

SLACK_SIGNING_SECRET = os.getenv('SIGNING_SECRET')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

package_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

handler = SlackRequestHandler(package_app)


@csrf_exempt
def package_events(request):
    if request.method == 'POST':
        if request.content_type == 'application/x-www-form-urlencoded':
            payload = request.POST.get('payload')
            if payload:
                return handler.handle(request)
    return JsonResponse({'status': 'ok'})


@package_app.action("open_modal_package_append")
def open_modal_package_append(ack, body, client):
    ack()
    user_id = body["user"]["id"]
    # print(body)
    blocks = package_modal.append_package_modal_block(user_id)
    modal_view = view_modal.create_modal_view_block(
        "패키지 등록", blocks, True, "append_package"
    )
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )
    except Exception as e:
        print(logger.error("Error fetching conversations: %s", e))


@package_app.view("append_package")
def db_append_package(ack, view, client, body):
    ack()
    view_state = view["state"]["values"]
    customer_name = view_state["select_customer"]["select_customer"]["selected_option"]["value"]
    package_name = view_state["input_package_name"]["input_package_name"]["value"]
    append_date = view_state["append_date"]["append_date"]["selected_date"]
    license_expire_date = view_state["license_expire_date"]["license_expire_date"]["selected_date"]
    os_type = view_state["os_type"]["os_type"]["selected_option"]["value"]

    customer_instance = Customer.objects.get(name=customer_name)

    try:
        Packages.objects.create(customer=customer_instance, name=package_name, created_at=append_date, license_expire_date=license_expire_date, platform=os_type)

    except Exception as e:
        print(logger.error("Error fetching conversations: %s", e))
        e = str(e)
        if "UNIQUE constraint failed" in e:
            msg = "동일한 OS의 패키지가 이미 있습니다."
        client.chat_postMessage(
            channel=body["user"]["id"],
            text=msg
        )


@package_app.action("open_modal_package_delete")
def open_modal_package_delete(ack, body, client: WebClient):
    ack()
    user_id = body["user"]["id"]
    # print(body)
    blocks = package_modal.package_delete_modal_block(user_id)
    modal_view = view_modal.create_modal_view_block(
        "패키지 삭제", blocks, True, "delete_package"
    )
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )
    except Exception as e:
        print(logger.error("Error fetching conversations: %s", e))


@package_app.action("update_modal_package_delete")
def update_modal_package_delete(ack, body, client: WebClient):
    print("update modal called")
    # print(body)
    user_id = body["user"]["id"]
    ack()
    selected_option = body['actions'][0]['selected_option']['value']
    # print(selected_option)
    blocks = package_modal.package_delete_modal_update_block(user_id, selected_option)
    updated_view = view_modal.create_modal_view_block(
        "패키지 삭제", blocks, True, "delete_package"
    )

    try:
        client.views_update(
            view_id=body["view"]["id"],
            view=updated_view,
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))


@package_app.view("delete_package")
def db_delete_package(ack, view, client, body):
    ack()
    view_state = view["state"]["values"]
    customer_name = util.get_selected_option_value(view_state, "update_modal_package_delete")
    package_name = util.get_selected_option_value(view_state, "select_package")
    os_type = util.get_selected_option_value(view_state, "os_type")
    delete_package = Packages.objects.get(customer_id=customer_name, name=package_name, platform=os_type)
    try:
        delete_package = Packages.objects.get(customer_id=customer_name, name=package_name, platform=os_type)
        delete_package.delete()
        print("Test")
    except Exception as e:
        print("error is :", e)
        print(logger.error("Error fetching conversations: %s", e))
        e = str(e)
        if "UNIQUE constraint failed" in e:
            msg = "머선일이고."
        client.chat_postMessage(
            channel=body["user"]["id"],
            text=msg
        )


@package_app.action("open_modal_packages_list")
def open_modal_packages_list(ack, body, client):
    ack()
    blocks = package_modal.package_list_modal_block()
    modal_view = view_modal.create_modal_view_block(
        "패키지 목록", blocks, False, "packages_list"
    )
    msg = DA.get_table("Packages")
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )
        client.chat_postMessage(
            channel=body["user"]["id"],
            text=msg
        )
    except SlackApiError as e:
        print(logger.error("Error fetching conversations: %s", e))
