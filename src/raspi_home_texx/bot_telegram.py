from abc import ABC, abstractmethod

import emoji
from typing import List

from . import get_console_logger, file_logger
from .automation import Automation
from .bot.chat_handler import ChatHandler
from .bot.chat_filter import ChatFilter
from .bot.commands import CommandCallback, Commands
from telegram import Bot
from telegram.error import BadRequest
from telegram.ext import Updater, CommandHandler


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
    __command_callbacks_auxiliary: [CommandCallback] = []

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
        # registers all handlers and filters
        self.__register_handlers()
        # start polling
        self.__updater.start_polling()

    def __register_handlers(self):
        # retrieve all callback functions
        callback_commands = self.__retrieve_callback_commands()
        # register all callbacks
        for command in callback_commands:
            command_handler = CommandHandler(
                command=command.command, callback=command.callback, filters=self.__chat_filter)
            self.__updater.dispatcher.add_handler(command_handler)

    def __retrieve_callback_commands(self) -> List[CommandCallback]:
        command_callbacks = [
            CommandCallback(self.__commands.CIAO, self.__chat_handler.ciao),
            CommandCallback(self.__commands.START, self.__chat_handler.start),
            CommandCallback(self.__commands.HELP, self.__chat_handler.help),
            CommandCallback(self.__commands.REBOOT, self.__chat_handler.reboot),
            CommandCallback(self.__commands.UPTIME, self.__chat_handler.uptime),
            CommandCallback(self.__commands.TEMPERATURE, self.__chat_handler.temperature_cpu),
            CommandCallback(self.__commands.SYSTEM_INFO, self.__chat_handler.system_info),
            CommandCallback(self.__commands.SEND_LOG, self.__chat_handler.send_log),
            CommandCallback(self.__commands.CLEAR_LOG, self.__chat_handler.clear_log),
            CommandCallback(self.__commands.ECU_CHECK, self.__chat_handler.ecu_check),
            CommandCallback(self.__commands.ALARM_CHECK, self.__chat_handler.alarm_check),
            CommandCallback(self.__commands.ECU_TOGGLE, self.__chat_handler.ecu_toggle),
            CommandCallback(self.__commands.ANTI_PANIC, self.__chat_handler.anti_panic),
            CommandCallback(self.__commands.GATE_CHECK, self.__chat_handler.gate_check),
            CommandCallback(self.__commands.GATE_TOGGLE, self.__chat_handler.gate_toggle),
            CommandCallback(self.__commands.GATE_STOP, self.__chat_handler.gate_stop)
        ]
        # append auxiliary commands
        command_callbacks.extend(self.__command_callbacks_auxiliary)

        return command_callbacks

    def append_command_callbacks(self, command_callbacks: [CommandCallback]):
        self.__command_callbacks_auxiliary.extend(command_callbacks)

    def send_message_to_list(self, msg: str):
        for chat_id in self.__list_id:
            try:
                self.__bot.send_message(chat_id=chat_id, text=msg)
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
        command_callbacks = self.create_command_callbacks(commands, chat_handler)

        bot = _BotTelegram(self._token, self._list_id)
        bot.set_automation_and_bind_alarm(self._automation)
        bot.set_commands(commands)
        bot.set_chat_handler(chat_handler)
        bot.set_chat_filter(chat_filter)
        bot.append_command_callbacks(command_callbacks)

        bot.register_handlers_and_start()

        return bot

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
    def create_command_callbacks(self, commands: Commands, chat_handler: ChatHandler) -> [CommandCallback]:
        pass
