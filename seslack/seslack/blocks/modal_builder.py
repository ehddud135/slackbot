from datetime import datetime
from seslack.blocks.DatabaseAccessor import DatabaseAccessor
from seslack.blocks.BlockGenerator import BlockGenerator

DA = DatabaseAccessor()
today_date = datetime.now().strftime('%Y-%m-%d')


def create_modal_view_block(input_text, blocks, include_submit=bool, callback_id=None):
    view = {
        "type": "modal",
                "callback_id": callback_id,
                "title": {"type": "plain_text", "text": input_text, "emoji": True},
                "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
                "blocks": blocks
    }
    if callback_id:
        view["callback_id"] = callback_id
    if include_submit:
        view["submit"] = {"type": "plain_text", "text": "Submit", "emoji": True}
    return view


def customer_append_modal_block():
    option_data = DA.get_options("manager_name", "ManagerList")
    option_data = [name[0] for name in option_data]
    # print(option_data)
    bg = BlockGenerator()
    bg.add_text_input("customer_name_input", "고객사명")
    bg.add_static_select("manager_name_input", "담당자명", option_data)
    bg.add_date_input("append_date", "등록일", today_date)
    blocks = bg.result
    return blocks


def customer_delete_modal_block(user_id):
    option_data = DA.get_options("manager_name", "ManagerList")
    option_data = [name[0] for name in option_data]
    bg = BlockGenerator()
    bg.add_static_select("select_manager", "담당자명", option_data)
    manager_name = DA.get_manager_name(user_id)
    blocks = bg.result
    return blocks

# Package 등록


def append_package_name_modal_block():
    os_type = ["AOS", "iOS"]
    bg = BlockGenerator()
    # bg.add_header("Pakcage Name")
    bg.add_text_input("input_package_name", "Package Name")
    bg.add_text_input("input_customer_name", "Customer Name")
    bg.add_date_input("append_date", "등록일", today_date)
    bg.add_date_input("license_expire_date", "라이센스 만료일", today_date)
    bg.add_radio_buttons("os_type", "os_type", os_type)
    blocks = bg.result
    return blocks


# SE 인원 등록
def append_manager_modal_block():
    bg = BlockGenerator()
    # bg.add_header("SE 등록")
    bg.add_text_input("input_manager_name", "이름")
    bg.add_date_input("append_date", "등록일", today_date)
    blocks = bg.result
    return blocks


def customer_list_modal_block():
    customer_list = DA.get_table("CustomerList")
    bg = BlockGenerator()
    bg.add_mrkdwn_block(customer_list)
    return bg.result
