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


class BotTelegram:
    __logger = None

    __list_id = None
    __bot = None
    __updater = None
    __dispatcher = None
    __chat_handler = None

    __automation = None
    __commands = None

    def __init__(self, token: str, name: str, list_id: List[int], automation: Automation):
        self.__logger = get_console_logger(self.__class__.__name__)
        self.__automation = automation
        self.__automation.bind_alarm_to(self.__send_alarm_state)
        # commands to bind
        self.__commands = Commands(name)
        # define list of all ids
        self.__list_id = list_id
        # create the bot
        self.__bot = Bot(token=token)
        self.__updater = Updater(token=token)
        # create the handler object
        self.__chat_handler = ChatHandler(self.__commands, self.__automation)
        # registers all handlers and filters
        self.__register_handlers()

        self.__updater.start_polling()

    def __register_handlers(self):
        self.__dispatcher = self.__updater.dispatcher

        callback_commands = self.__retrieve_callback_commands()
        # register all callbacks
        for command in callback_commands:
            self.__register_handler(command.command, command.callback)

    def __retrieve_callback_commands(self):
        return [
            CommandCallback(self.__commands.CIAO, self.__chat_handler.ciao),
            CommandCallback(self.__commands.START, self.__chat_handler.start),
            CommandCallback(self.__commands.HELP, self.__chat_handler.help),
            CommandCallback(self.__commands.UPTIME, self.__chat_handler.uptime),
            CommandCallback(self.__commands.TEMPERATURE, self.__chat_handler.temperature_cpu),
            CommandCallback(self.__commands.SYSTEM_INFO, self.__chat_handler.system_info),
            CommandCallback(self.__commands.SEND_LOG, self.__chat_handler.send_log),
            CommandCallback(self.__commands.CLEAR_LOG, self.__chat_handler.clear_log),
            CommandCallback(self.__commands.REBOOT, self.__chat_handler.reboot),
            CommandCallback(self.__commands.UPDATE_UPGRADE, self.__chat_handler.update_upgrade),
            CommandCallback(self.__commands.ECU_CHECK, self.__chat_handler.ecu_check),
            CommandCallback(self.__commands.ALARM_CHECK, self.__chat_handler.alarm_check),
            CommandCallback(self.__commands.ECU_TOGGLE, self.__chat_handler.ecu_toggle),
            CommandCallback(self.__commands.ANTI_PANIC, self.__chat_handler.anti_panic),
            CommandCallback(self.__commands.GATE_CHECK, self.__chat_handler.gate_check),
            CommandCallback(self.__commands.GATE_TOGGLE, self.__chat_handler.gate_toggle),
            CommandCallback(self.__commands.GATE_STOP, self.__chat_handler.gate_stop),
        ]

    def __register_handler(self, command: str, callback):
        chat_filter = ChatFilter(self.__list_id)
        self.__dispatcher.add_handler(CommandHandler(command=command, callback=callback, filters=chat_filter))

    def send_message_to_list(self, msg: str):
        for chat_id in self.__list_id:
            try:
                self.__bot.send_message(chat_id=chat_id, text=msg)
            except BadRequest as err:
                self.__logger.exception("error on send message: " + err.__str__())
                file_logger.write("Error on send message to: " + str(chat_id))
            except Exception as err:
                self.__logger.exception("errore invio telegram: " + err.__str__())
                file_logger.write("errore di invio telegram")

    def __send_alarm_state(self, is_alarm_ringing: bool):
        if is_alarm_ringing:
            snt = emoji.emojize("Allarme sta suonando :rotating_light:", use_aliases=True)
        else:
            snt = emoji.emojize("Allarme rientrato :green_circle:", use_aliases=True)

        self.send_message_to_list(snt)