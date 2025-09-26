from abc import ABC, abstractmethod

import emoji
from typing import List

from . import get_console_logger, file_logger
from .automation import Automation
from .bot.chat_handler import ChatHandler
from .bot.chat_filter import ChatFilter
from .bot.commands import CommandCallback, Commands, MessageCallback
from telegram import Bot, ReplyKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

from .bot.custom_keyboard_builder import SimpleKeyboardBuilder


class BotTelegram(ABC):
    _logger = None

    def __init__(self, logger):
        self._logger = logger

    @abstractmethod
    def send_message_to_list(self, msg: str):
        pass


class _BotTelegram(BotTelegram):
    __list_id: List[int] = None
    __bot: Bot = None
    __updater: Updater = None
    __command_callbacks_auxiliary: list[CommandCallback] = []
    __message_callbacks_auxiliary: list[MessageCallback] = []
    __custom_keyboard: ReplyKeyboardMarkup = None

    __automation: Automation = None
    __commands: Commands = None
    __chat_handler: ChatHandler = None
    __chat_filter: ChatFilter = None

    def __init__(self, token: str, list_id: List[int]):
        super().__init__(get_console_logger(self.__class__.__name__))
        # define list of all ids
        self.__list_id = list_id
        # create the bot
        self.__bot = Bot(token=token)
        self.__updater = Updater(token=token)

    def set_custom_keyboard(self, custom_keyboard: ReplyKeyboardMarkup):
        self.__custom_keyboard = custom_keyboard

    def set_automation_and_bind_alarm(self, automation: Automation):
        self.__automation = automation
        self.__automation.bind_alarm_to(self.__send_alarm_state)

    def set_commands(self, commands: Commands):
        self.__commands = commands

    def set_chat_handler(self, chat_handler: ChatHandler):
        self.__chat_handler = chat_handler

    def set_chat_filter(self, chat_filter: ChatFilter):
        self.__chat_filter = chat_filter

    def register_handlers_and_start(self):
        # register commands handlers
        self.__register_command_handlers()
        # register messages handlers
        self.__register_message_handler()
        # start polling
        self.__updater.start_polling()

    def __register_command_handlers(self):
        # retrieve all callback functions
        callback_commands = self.__retrieve_callback_commands()
        # register all callbacks
        for command in callback_commands:
            command_handler = CommandHandler(
                command=command.get_commands(),
                callback=command.get_callback(),
                filters=self.__chat_filter)
            self.__updater.dispatcher.add_handler(command_handler)

    def __retrieve_callback_commands(self) -> List[CommandCallback]:
        command_callbacks = [
            CommandCallback(Commands.CIAO, self.__chat_handler.ciao),
            CommandCallback(Commands.START, self.__chat_handler.start),
            CommandCallback(Commands.HELP, self.__chat_handler.help),
            CommandCallback(Commands.UPTIME, self.__chat_handler.uptime),
            CommandCallback(Commands.TEMPERATURE, self.__chat_handler.temperature_cpu),
            CommandCallback(Commands.SYSTEM_INFO, self.__chat_handler.system_info),
            CommandCallback(Commands.SEND_LOG, self.__chat_handler.send_log),
            CommandCallback(Commands.CLEAR_LOG, self.__chat_handler.clear_log),
            CommandCallback(Commands.ECU_CHECK, self.__chat_handler.ecu_check),
            CommandCallback(Commands.ALARM_CHECK, self.__chat_handler.alarm_check),
            CommandCallback(Commands.ECU_TOGGLE, self.__chat_handler.ecu_toggle),
            CommandCallback(Commands.ANTI_PANIC, self.__chat_handler.anti_panic),
            CommandCallback(Commands.GATE_CHECK, self.__chat_handler.gate_check),
            CommandCallback(Commands.GATE_TOGGLE, self.__chat_handler.gate_toggle),
            CommandCallback(Commands.GATE_STOP, self.__chat_handler.gate_stop)
        ]
        # append auxiliary commands
        command_callbacks.extend(self.__command_callbacks_auxiliary)

        return command_callbacks

    def __register_message_handler(self):
        self.__updater.dispatcher.add_handler(MessageHandler(filters=self.__chat_filter, callback=self.__handle_message))

    def __handle_message(self, update: Update, context: CallbackContext):
        text = update.message.text
        for message_callback in self.__message_callbacks_auxiliary:
            if message_callback.get_message() == text:
                callback = message_callback.get_callback()
                callback(update, context)

                return

    def append_command_callbacks(self, command_callbacks: [CommandCallback]):
        self.__command_callbacks_auxiliary.extend(command_callbacks)

    def append_message_callbacks(self, message_callbacks: [MessageCallback]):
        self.__message_callbacks_auxiliary.extend(message_callbacks)

    def send_message_to_list(self, msg: str):
        for chat_id in self.__list_id:
            try:
                self.__bot.send_message(chat_id=chat_id, text=msg, reply_markup=self.__custom_keyboard)
            except BadRequest as err:
                self._logger.exception("error on send message: " + err.__str__())
                file_logger.write("Error on send message to: " + str(chat_id))
            except Exception as err:
                self._logger.exception("errore invio telegram: " + err.__str__())
                file_logger.write("errore di invio telegram")

    def __send_alarm_state(self, is_alarm_ringing: bool):
        if is_alarm_ringing:
            snt = emoji.emojize("Allarme sta suonando :rotating_light:", use_aliases=True)
        else:
            snt = emoji.emojize("Allarme rientrato :green_circle:", use_aliases=True)

        self.send_message_to_list(snt)


class AbstractBotTelegramBuilder(ABC):

    def __init__(self):
        self._list_id = None
        self._token = None
        self._name = None
        self._automation = None

    def set_list_id(self, list_id: List[int]):
        self._list_id = list_id
        return self

    def set_token(self, token: str):
        self._token = token
        return self

    def set_name(self, name: str):
        self._name = name
        return self

    def set_automation(self, automation: Automation):
        self._automation = automation
        return self

    def build(self) -> _BotTelegram:
        commands = self.create_commands(self._name)
        chat_handler = self.create_handler(commands, self._automation)
        chat_filter = self.create_chat_filter(self._list_id)
        command_callbacks = self.create_command_callbacks(chat_handler)
        message_callbacks = self.create_message_callbacks(chat_handler)
        custom_keyboard = self.create_custom_keyboard(chat_handler)

        bot = _BotTelegram(self._token, self._list_id)
        bot.set_automation_and_bind_alarm(self._automation)
        bot.set_commands(commands)
        bot.set_chat_handler(chat_handler)
        bot.set_chat_filter(chat_filter)
        bot.set_custom_keyboard(custom_keyboard)
        bot.append_command_callbacks(command_callbacks)
        bot.append_message_callbacks(message_callbacks)

        bot.register_handlers_and_start()

        return bot

    def create_custom_keyboard(self, chat_handler: ChatHandler) -> ReplyKeyboardMarkup:
        return SimpleKeyboardBuilder(chat_handler).build()

    @abstractmethod
    def create_commands(self, name: str) -> Commands:
        pass

    @abstractmethod
    def create_handler(self, commands: Commands, automation: Automation) -> ChatHandler:
        pass

    @abstractmethod
    def create_chat_filter(self, list_id: List[int]) -> ChatFilter:
        pass

    @abstractmethod
    def create_command_callbacks(self, chat_handler: ChatHandler) -> list[CommandCallback]:
        pass

    @abstractmethod
    def create_message_callbacks(self, chat_handler: ChatHandler) -> list[MessageCallback]:
        pass
