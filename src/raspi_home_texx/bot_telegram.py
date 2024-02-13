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


class _BotTelegram:
    _logger = None

    _list_id = None
    _bot = None
    _updater = None
    _dispatcher = None

    _automation = None
    _commands = None
    _chat_handler = None
    _chat_filter = None

    def __init__(self, token: str, list_id: List[int]):
        self._logger = get_console_logger(self.__class__.__name__)
        # define list of all ids
        self._list_id = list_id
        # create the bot
        self._bot = Bot(token=token)
        self._updater = Updater(token=token)

    def set_automation_and_bind_alarm(self, automation: Automation):
        self._automation = automation
        self._automation.bind_alarm_to(self.__send_alarm_state)

    def register_handlers_and_start(self):
        # registers all handlers and filters
        self.__register_handlers()
        # start polling
        self._updater.start_polling()

    def __register_handlers(self):
        self._dispatcher = self._updater.dispatcher

        callback_commands = self.__retrieve_callback_commands()
        # register all callbacks
        for command in callback_commands:
            command_handler = CommandHandler(
                command=command.command, callback=command.callback, filters=self._chat_filter)
            self._dispatcher.add_handler(command_handler)

    def __retrieve_callback_commands(self):
        return [
            CommandCallback(self._commands.CIAO, self._chat_handler.ciao),
            CommandCallback(self._commands.START, self._chat_handler.start),
            CommandCallback(self._commands.HELP, self._chat_handler.help),
            CommandCallback(self._commands.UPTIME, self._chat_handler.uptime),
            CommandCallback(self._commands.TEMPERATURE, self._chat_handler.temperature_cpu),
            CommandCallback(self._commands.SYSTEM_INFO, self._chat_handler.system_info),
            CommandCallback(self._commands.SEND_LOG, self._chat_handler.send_log),
            CommandCallback(self._commands.CLEAR_LOG, self._chat_handler.clear_log),
            CommandCallback(self._commands.REBOOT, self._chat_handler.reboot),
            CommandCallback(self._commands.UPDATE_UPGRADE, self._chat_handler.update_upgrade),
            CommandCallback(self._commands.ECU_CHECK, self._chat_handler.ecu_check),
            CommandCallback(self._commands.ALARM_CHECK, self._chat_handler.alarm_check),
            CommandCallback(self._commands.ECU_TOGGLE, self._chat_handler.ecu_toggle),
            CommandCallback(self._commands.ANTI_PANIC, self._chat_handler.anti_panic),
            CommandCallback(self._commands.GATE_CHECK, self._chat_handler.gate_check),
            CommandCallback(self._commands.GATE_TOGGLE, self._chat_handler.gate_toggle),
            CommandCallback(self._commands.GATE_STOP, self._chat_handler.gate_stop),
        ]

    def send_message_to_list(self, msg: str):
        for chat_id in self._list_id:
            try:
                self._bot.send_message(chat_id=chat_id, text=msg)
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

    def set_token(self, token: str):
        self._token = token

    def set_name(self, name: str):
        self._name = name

    def set_automation(self, automation: Automation):
        self._automation = automation

    def build(self) -> _BotTelegram:
        commands = self.create_commands(self._name)
        chat_handler = self.create_handler(commands, self._automation)
        chat_filter = self.create_chat_filter(self._list_id)

        bot = _BotTelegram(self._token, self._list_id)
        bot.set_automation_and_bind_alarm(self._automation)
        bot._commands = commands
        bot._chat_handler = chat_handler
        bot._chat_filter = chat_filter

        bot.register_handlers_and_start()

        return bot

    @abstractmethod
    def create_commands(self, name) -> Commands:
        pass

    @abstractmethod
    def create_handler(self, commands: Commands, automation: Automation) -> ChatHandler:
        pass

    @abstractmethod
    def create_chat_filter(self, list_id: List[int]) -> ChatFilter:
        pass
