import emoji
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from .chat_handler import ChatHandler


class CustomKeyboardBuilder:
    ecu_gate_btn = None
    gate_toggle_btn = None

    ecu_check_btn = None
    gate_check_btn = None

    def __init__(self, chat_handler: ChatHandler):
        self.ecu_toggle_btn = self.__create_ecu_toggle_btn(chat_handler)
        self.gate_toggle_btn = self.__create_gate_toggle_btn(chat_handler)

        self.ecu_check_btn = self.__create_ecu_check_btn(chat_handler)
        self.gate_check_btn = self.__create_gate_check_btn(chat_handler)

    def __create_ecu_toggle_btn(self, chat_handler: ChatHandler) -> InlineKeyboardButton:
        text = emoji.emojize(":house: Ecu Toggle'")
        data = '/' + chat_handler.ecu_toggle.__name__

        return InlineKeyboardButton(text=text, callback_data=data)

    def __create_gate_toggle_btn(self, chat_handler: ChatHandler) -> InlineKeyboardButton:
        text = emoji.emojize(":door: Gate Toggle")
        data = chat_handler.gate_toggle.__name__

        return InlineKeyboardButton(text=text, callback_data=data)

    def __create_ecu_check_btn(self, chat_handler: ChatHandler) -> InlineKeyboardButton:
        text = emoji.emojize(":information: :house: Ecu Check")
        data = chat_handler.ecu_check.__name__

        return InlineKeyboardButton(text=text, callback_data=data)

    def __create_gate_check_btn(self, chat_handler: ChatHandler) -> InlineKeyboardButton:
        text = emoji.emojize(':information: :door: Gate Check')
        data = chat_handler.gate_check.__name__

        return InlineKeyboardButton(text=text, callback_data=data)

    def build(self) -> InlineKeyboardMarkup:
        keyboard = [
            [self.ecu_toggle_btn, self.gate_toggle_btn],
            [self.ecu_check_btn, self.gate_check_btn]
        ]

        return InlineKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
