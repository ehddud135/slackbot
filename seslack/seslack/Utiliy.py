
class Utiliy():
    def __init__(self) -> None:
        pass

    def get_selected_option_value(self, view_state, options_name):
        result = view_state[options_name][options_name]["selected_option"]["value"]
        return result
