import sqlite3
import pandas as pd
from tabulate import tabulate
from customer.models import CustomerList

dbconn = sqlite3.connect(r"D:\automation\slack_bot\seslack\db.sqlite3")

df = pd.read_sql("SELECT * FROM customer_customerlist", dbconn, index_col=None)

# print(df)

# print(tabulate(df, headers='keys', tablefmt='psql', showindex=True))
result = tabulate(df, headers='keys', tablefmt='psql', showindex=True)


def home_tab_blocks(data):

    blocks = [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "고객사 등록"},
                    "action_id": "open_modal"
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Approve Button", "emoji": True},
                    "value": "click_me_123",
                    "action_id": "approve_test"
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Ler Ros", "emoji": True},
                    "value": "click_me_123",
                    "url": "https://google.com"
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
            "type": "input",
            "element": {"type": "plain_text_input", "action_id": "plain_text_input-action"},
            "label": {"type": "plain_text", "text": "Label", "emoji": True}
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                    "type": "mrkdwn",
                    "text": f"{result}"
            }
        }
    ]
    for item in data:
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Name: {item.customer_name}, Age: {item.manager}"
                }
            }
        )

    return blocks
