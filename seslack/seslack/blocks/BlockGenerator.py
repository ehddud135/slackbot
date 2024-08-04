

class BlockGenerator:
    def __init__(self):
        self.blocks = []

    def add_header(self, input_text):
        self.blocks.append(
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"{input_text}", "emoji": True}
            }
        )

    def add_text_input(self, block_id, input_text):
        self.blocks.append(
            {
                "type": "input",
                "block_id": block_id,
                "element": {"type": "plain_text_input", "action_id": block_id},
                "label": {"type": "plain_text", "text": input_text, "emoji": True}
            }
        )

    def add_date_input(self, block_id, input_text, date):
        self.blocks.append(
            {
                "type": "input",
                "block_id": block_id,
                "element": {"type": "datepicker", "action_id": block_id, "initial_date": date},
                "label": {"type": "plain_text", "text": input_text, "emoji": True}
            }
        )

    def add_static_select(self, block_id, input_text, option_name_list):
        option_block = self.make_options_block(option_name_list)
        self.blocks.append(
            {
                "type": "input",
                "block_id": block_id,
                "element": {"type": "static_select", "placeholder": {"type": "plain_text", "text": "Select an item"},
                            "options": option_block, "action_id": block_id},
                "label": {"type": "plain_text", "text": input_text}
            }
        )

    def add_button(self, input_text, action_id):
        self.blocks.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": input_text},
                "action_id": action_id
            }
        )

    def add_radio_buttons(self, block_id, input_text, option_name_list):
        options_block = self.make_options_block(option_name_list)
        self.blocks.append(
            {
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
        )

    def add_mrkdwn_block(self, result):
        self.blocks.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"```{result}```"}
            }
        )

    def make_options_block(self, option_list):
        result = []
        for option in option_list:
            option_block = {
                "text": {"type": "plain_text", "text": option},
                "value": option
            }
            result.append(option_block)
        return result

    @property
    def result(self):
        return self.blocks
