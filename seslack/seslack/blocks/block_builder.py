from datetime import datetime
from seslack.blocks.DatabaseAccessor import DatabaseAccessor
from seslack.blocks.BlockGenerator import BlockGenerator

DA = DatabaseAccessor()

today_date = datetime.now().strftime('%Y-%m-%d')


def home_tab_blocks():
    result = DA.get_table("Customer")
    top_block = top_action_block()
    bottom_block = bottom_action_block()
    blocks = [
        {"type": "actions", "elements": top_block},
        {"type": "divider"},
        {"type": "header",
         "text": {"type": "plain_text", "text": "정기점검 관리", "emoji": True}
         },
        {"type": "divider"},
        {"type": "section",
         "text": {"type": "mrkdwn", "text": f"```{result}```"}
         },
        {"type": "divider"},
        {"type": "actions",
         "elements": bottom_block}
    ]

    return blocks


def make_options_block(option_data):
    result = []
    for option in option_data:
        option_block = {
            "text": {"type": "plain_text", "text": option[0]},
            "value": option[0]
        }
        result.append(option_block)
    return result


def top_action_block():
    bg = BlockGenerator()
    bg.add_button("고객사 등록", "open_modal_customer_append")
    bg.add_button("Approve Button", "approve_test")
    bg.add_button("고객사 삭제", "open_modal_customer_delete")
    bg.add_button("패키지 명 등록", "open_modal_package_append")
    # bg.add_button("SE 등록", "open_modal_append_manager")
    return bg.result


def bottom_action_block():
    bg = BlockGenerator()
    bg.add_button("고객사 목록", "open_modal_customer_list")
    bg.add_button("Approve Button", "approve_test")
    bg.add_button("점검 내역", "open_modal_customer_delete")
    bg.add_button("패키지 명 목록", "open_modal_package_append")
    # bg.add_button("SE 등록", "open_modal_append_manager")
    return bg.result
