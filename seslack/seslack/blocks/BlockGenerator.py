

class BlockGenerator:
    def __init__(self):
        self.blocks = []

    def add_header(self, input_text):
        block = {
            "type": "header",
            "text": {"type": "plain_text", "text": f"{input_text}", "emoji": True}
        }
        self.blocks.append(block)

    def add_text_input(self, block_id, input_text):
        block = {
            "type": "input",
            "block_id": block_id,
            "element": {"type": "plain_text_input", "action_id": block_id},
            "label": {"type": "plain_text", "text": input_text, "emoji": True}
        }
        self.blocks.append(block)

    def add_date_input(self, block_id, input_text, date):
        block = {
            "type": "input",
            "block_id": block_id,
            "element": {"type": "datepicker", "action_id": block_id, "initial_date": date},
            "label": {"type": "plain_text", "text": input_text, "emoji": True}
        }
        self.blocks.append(block)

    def add_input_static_select(self, block_id, input_text, option_name_list, dispatch=False):
        option_block = self.add_make_options_block(option_name_list)
        block = {
            "type": "input",
            "block_id": block_id,
            "element": {"type": "static_select", "placeholder": {"type": "plain_text", "text": "Select an item"},
                        "options": option_block, "action_id": block_id},
            "label": {"type": "plain_text", "text": input_text}
        }
        if dispatch:
            block["dispatch_action"] = True
        self.blocks.append(block)

    def add_button(self, input_text, action_id):
        block = {
            "type": "button",
            "text": {"type": "plain_text", "text": input_text},
            "action_id": action_id
        }
        self.blocks.append(block)

    def add_radio_buttons(self, block_id, input_text, option_name_list):
        options_block = self.add_make_options_block(option_name_list)
        block = {
            "type": "input",
            "block_id": block_id,
            "element": {
                "type": "radio_buttons",
                "options": options_block,
                "action_id": block_id
            },
            "label": {
                "type": "plain_text",
                "text": input_text,
                "emoji": True
            }
        }
        self.blocks.append(block)

    def add_mrkdwn_block(self, result):
        block = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"```{result}```"}
        }
        self.blocks.append(block)

    def add_make_options_block(self, option_list):
        result = []
        for option in option_list:
            option_block = {
                "text": {"type": "plain_text", "text": option},
                "value": option
            }
            result.append(option_block)
        return result

    def add_check_box_block(self, block_id, option_list, input_text):
        options_block = self.add_make_options_block(option_list)
        block = {
            "type": "input",
            "block_id": block_id,
            "element": {"type": "checkboxes", "options": options_block, "action_id": block_id},
            "label": {"type": "plain_text", "text": input_text, "emoji": True}
        }
        self.blocks.append(block)

    def add_error_block(self, error):
        block = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f":warning: *Error:* {str(error)}"}
        }
        self.blocks.append(block)

    @property
    def result(self):
        return self.blocks
