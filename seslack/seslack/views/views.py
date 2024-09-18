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
from django.shortcuts import redirect
from customer.models import Customer, Manager, Packages
from ..blocks import block_builder
from ..views import customer_views, manager_views, package_views, inspect_views

env_path = "../../.env"
load_dotenv(dotenv_path=env_path)

view_block = block_builder

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

SLACK_SIGNING_SECRET = os.getenv('SIGNING_SECRET')
SLACK_BOT_TOKEN = os.getenv('BOT_TOKEN')

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
            data = json.loads(payload)
            if data.get('type') == 'url_verification':
                return JsonResponse({'challenge': data['challenge']})
            return handler.handle(request)
        elif request.content_type == 'application/x-www-form-urlencoded':
            payload = request.POST.get('payload')
            if payload:
                data = json.loads(payload)
                # print(data)
                action_type = data["type"]
                if action_type == "view_submission":
                    id = data["view"]["callback_id"]
                elif action_type == "block_actions":
                    id = data["actions"][0]["action_id"]
                if "customer" in id:
                    return customer_views.customer_events(request)
                elif "manager" in id:
                    return manager_views.manager_events(request)
                elif "package" in id:
                    return package_views.package_events(request)
                elif "inspect" in id:
                    return inspect_views.inspect_events(request)
                else:
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
