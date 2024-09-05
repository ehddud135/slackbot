from datetime import datetime
from seslack.blocks.DatabaseAccessor import DatabaseAccessor
from seslack.blocks.BlockGenerator import BlockGenerator

DA = DatabaseAccessor()
today_date = datetime.now().strftime('%Y-%m-%d')


def customer_append_modal_block():
    option_data = DA.get_options("name", "Manager")
    # print(option_data)
    bg = BlockGenerator()
    bg.add_text_input("customer_name_input", "고객사명")
    bg.add_input_static_select("manager_name_input", "담당자명", option_data)
    bg.add_date_input("append_date", "등록일", today_date)
    blocks = bg.result
    return blocks


def customer_delete_modal_block(user_id):
    manager_option = DA.get_options("name", "Manager")
    customer_option = DA.get_options("name", "Customer")
    bg = BlockGenerator()
    bg.add_input_static_select("update_modal_customer_delete", "담당자명", manager_option, True)
    bg.add_input_static_select("select_customer", "고객사명", customer_option)
    blocks = bg.result
    return blocks


def customer_delete_modal_update_block(select_option):
    manager_option = DA.get_options("name", "Manager")
    selectd_option = f"manager_id='{select_option}'"
    customer_option = DA.get_options("name", "Customer", selectd_option)
    bg = BlockGenerator()
    bg.add_input_static_select("update_modal_customer_delete", "담당자명", manager_option, True)
    bg.add_input_static_select("select_customer", "고객사명", customer_option)
    blocks = bg.result
    return blocks


def customer_list_modal_block():
    customer_list = DA.get_table("Customer")
    bg = BlockGenerator()
    bg.add_mrkdwn_block(customer_list)
    return bg.result
