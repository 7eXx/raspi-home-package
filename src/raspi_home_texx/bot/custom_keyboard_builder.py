
from telegram import KeyboardButton, ReplyKeyboardMarkup
from .chat_handler import ChatHandler


class CustomKeyboardBuilder:
    ecu_gate_btn = None
    gate_toggle_btn = None

    ecu_check_btn = None
    gate_check_btn = None

    def __init__(self, chat_handler: ChatHandler):
        self.ecu_toggle_btn = KeyboardButton('/' + chat_handler.ecu_toggle.__name__)
        self.gate_toggle_btn = KeyboardButton('/' + chat_handler.gate_toggle.__name__)

        self.ecu_check_btn = KeyboardButton('/' + chat_handler.ecu_check.__name__)
        self.gate_check_btn = KeyboardButton('/' + chat_handler.gate_check.__name__)

    def build(self) -> ReplyKeyboardMarkup:
        keyboard = [
            [self.ecu_toggle_btn, self.gate_toggle_btn],
            [self.ecu_check_btn, self.gate_check_btn]
        ]

        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
