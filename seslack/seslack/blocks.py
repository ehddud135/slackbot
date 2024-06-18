import sqlite3
import pandas as pd
from tabulate import tabulate
from customer.models import CustomerList


def home_tab_blocks():
    dbconn = sqlite3.connect(r"C:\Users\HwangDongYeong\Documents\GitHub\slackbot\seslack\db.sqlite3")
    df = pd.read_sql("SELECT * FROM customer_customerlist", dbconn, index_col=None)
    df = df.drop(labels='id', axis=1)
    result = tabulate(df, headers='keys', tablefmt='heavy_grid', showindex=False)
    print(result)

    blocks = [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "고객사 등록"},
                    "action_id": "open_modal_customer_append"
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Approve Button", "emoji": True},
                    "action_id": "approve_test"
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "고객사 삭제"},
                    "action_id": "open_modal_customer_delete"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "정기점검 관리", "emoji": True}
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                    "type": "mrkdwn",
                    "text": f"```{result}```"
            }
        }
    ]

    return blocks


def customer_append_modal_block():
    blocks = [
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
        },
        {
            "type": "input",
            "block_id": "append_date",
                        "element": {"type": "plain_text_input", "action_id": "append_date"},
                        "label": {"type": "plain_text", "text": "담당자명", "emoji": True}
        }
    ]
    return blocks


def customer_delete_modal_block(user_id):
    blocks = [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "conversations_select",
                    "placeholder": {"type": "plain_text", "text": "Select private conversation", "emoji": True},
                    "filter": {"include": ["private"]},
                    "action_id": "customer_delete"
                }
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "conversations_select",
                    "placeholder": {"type": "plain_text", "text": "Select a conversation"},
                    "initial_conversation": "G12345678",
                    "action_id": "actionId-0"
                },
                {
                    "type": "users_select",
                    "placeholder": {"type": "plain_text", "text": "Select a user"},
                    "initial_user": f"{user_id}",
                                    "action_id": "actionId-1"
                },
                {
                    "type": "channels_select",
                    "placeholder": {"type": "plain_text", "text": "Select a channel"},
                    "initial_channel": "C12345678",
                    "action_id": "actionId-2"
                }
            ]
        },
    ]
    return blocks
