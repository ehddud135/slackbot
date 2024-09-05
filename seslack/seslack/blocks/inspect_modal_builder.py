from datetime import datetime
from seslack.blocks.DatabaseAccessor import DatabaseAccessor
from seslack.blocks.BlockGenerator import BlockGenerator

DA = DatabaseAccessor()
today_date = datetime.now().strftime('%Y-%m-%d')


def modify_inspect_schedule_modal_block():
    option_data = DA.get_options("name", "Customer")
    schedule_list_1 = ["January", "February", "March", "April", "May", "June"]
    schedule_list_2 = ["July", "August", "September", "October", "November", "December"]
    bg = BlockGenerator()
    bg.add_input_static_select("customer_name_input", "고객사명", option_data)
    bg.add_check_box_block("inspect_schedule_1", schedule_list_1, "점검 일정을 선택해주세요")
    bg.add_check_box_block("inspect_schedule_2", schedule_list_2, "점검 일정을 선택해주세요")
    return bg.result
