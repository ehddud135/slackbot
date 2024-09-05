from datetime import datetime
from seslack.blocks.DatabaseAccessor import DatabaseAccessor
from seslack.blocks.BlockGenerator import BlockGenerator

DA = DatabaseAccessor()
today_date = datetime.now().strftime('%Y-%m-%d')

# SE 인원 등록


def append_manager_modal_block():
    bg = BlockGenerator()
    bg.add_header("SE 등록")
    bg.add_text_input("input_manager_name", "이름")
    bg.add_date_input("append_date", "등록일", today_date)
    return bg.result
