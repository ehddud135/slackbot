from datetime import datetime
from seslack.blocks.DatabaseAccessor import DatabaseAccessor
from seslack.blocks.BlockGenerator import BlockGenerator

DA = DatabaseAccessor()
today_date = datetime.now().strftime('%Y-%m-%d')


def append_package_modal_block(user_id, error=False, error_msg=None):
    os_type = ["AOS", "iOS"]
    manager_name = DA.get_manager_name(user_id)
    manager_option = f"manager_id='{manager_name}'"
    customer_option = DA.get_options("name", "Customer", manager_option)
    bg = BlockGenerator()
    if error:
        bg.add_error_block(error_msg)
    # bg.add_header("Pakcage Name")
    bg.add_input_static_select("select_customer", "고객사명", customer_option)
    bg.add_text_input("input_package_name", "Package Name")
    bg.add_date_input("append_date", "등록일", today_date)
    bg.add_date_input("license_expire_date", "라이센스 만료일", today_date)
    bg.add_radio_buttons("os_type", "Platform", os_type)
    return bg.result


# SE 인원 등록
def append_manager_modal_block():
    bg = BlockGenerator()
    # bg.add_header("SE 등록")
    bg.add_text_input("input_manager_name", "이름")
    bg.add_date_input("append_date", "등록일", today_date)
    return bg.result


def package_delete_modal_block(user_id):
    manager_name = DA.get_manager_name(user_id)
    manager_option = f"manager_id='{manager_name}'"
    customer_option = DA.get_options("name", "Customer", manager_option)
    bg = BlockGenerator()
    bg.add_input_static_select("update_modal_package_delete", "고객사명", customer_option, True)
    return bg.result


def package_delete_modal_update_block(user_id, select_option):
    os_type = ["AOS", "iOS"]
    manager_name = DA.get_manager_name(user_id)
    manager_option = f"manager_id='{manager_name}'"
    selectd_option = f"customer_id='{select_option}'"
    customer_option = DA.get_options("name", "Customer", manager_option)
    package_option = DA.get_options("name", "Packages", selectd_option)
    bg = BlockGenerator()
    bg.add_input_static_select("update_modal_package_delete", "고객사 명", customer_option, True)
    bg.add_input_static_select("select_package", "패키지 명", package_option, True)
    bg.add_radio_buttons("os_type", "Platform", os_type)
    blocks = bg.result
    return blocks


def package_list_modal_block():
    pakcage_list = DA.get_table("Packages")
    bg = BlockGenerator()
    bg.add_mrkdwn_block(pakcage_list)
    return bg.result
