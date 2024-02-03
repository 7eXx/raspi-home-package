import emoji
from typing import List

from . import create_logger
from .automation import Automation
from .bot.chat_handler import ChatHandler
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

    def __init__(self, bot_token, list_id: List[int], automation: Automation):
        self.__logger = create_logger(self.__class__.__name__)
        self.__automation = automation
        self.__automation.bind_alarm_to(self.__send_alarm_state)
        # define list of all ids
        self.__list_id = list_id
        # create the bot
        self.__bot = Bot(token=bot_token)
        self.__updater = Updater(token=bot_token)
        # create the handler object
        self.__chat_handler = ChatHandler(self.__automation)
        # registers all handlers and filters
        self.__register_handlers()

        self.__updater.start_polling()

    def __register_handlers(self):
        self.__dispatcher = self.__updater.dispatcher

        callback_list = self.__retrieve_callback_list()
        # register all callbacks
        for callback in callback_list:
            self.__register_handler(callback.command, callback.callback)

    def __retrieve_callback_list(self):
        return [
            CommandCallback(Command.CIAO, self.__chat_handler.ciao),
            CommandCallback(Command.START, self.__chat_handler.start),
            CommandCallback(Command.HELP, self.__chat_handler.help),
            CommandCallback(Command.UPTIME, self.__chat_handler.uptime),
            CommandCallback(Command.TEMPERATURE, self.__chat_handler.temperature_cpu),
            CommandCallback(Command.SYSTEM_INFO, self.__chat_handler.system_info),
            CommandCallback(Command.SEND_LOG, self.__chat_handler.send_log),
            CommandCallback(Command.CLEAR_LOG, self.__chat_handler.clear_log),
            CommandCallback(Command.REBOOT, self.__chat_handler.reboot),
            CommandCallback(Command.UPDATE_UPGRADE, self.__chat_handler.update_upgrade),
            CommandCallback(Command.ECU_CHECK, self.__chat_handler.ecu_check),
            CommandCallback(Command.ALARM_CHECK, self.__chat_handler.alarm_check),
            CommandCallback(Command.ECU_TOGGLE, self.__chat_handler.ecu_toggle),
            CommandCallback(Command.ANTI_PANIC, self.__chat_handler.anti_panic),
            CommandCallback(Command.GATE_CHECK, self.__chat_handler.gate_check),
            CommandCallback(Command.GATE_TOGGLE, self.__chat_handler.gate_toggle),
            CommandCallback(Command.GATE_STOP, self.__chat_handler.gate_stop),
        ]

    def __register_handler(self, command: str, callback):
        chat_filter = HomeChatFilter(self.__list_id)
        self.__dispatcher.add_handler(CommandHandler(command=command, callback=callback, filters=chat_filter))

    def send_message_to_list(self, msg: str):
        for chat_id in self.__list_id:
            try:
                self.__bot.send_message(chat_id=chat_id, text=msg)
            except BadRequest as err:
                self.__logger.exception("error on send message: " + err.__str__())
                DiskLogger.write("Error on send message to: " + str(chat_id))
            except Exception as err:
                self.__logger.exception("errore invio telegram: " + err.__str__())
                DiskLogger.write("errore di invio telegram")

    def __send_alarm_state(self, is_alarm_ringing: bool):
        if is_alarm_ringing:
            snt = emoji.emojize("Allarme sta suonando :rotating_light:", use_aliases=True)
        else:
            snt = emoji.emojize("Allarme rientrato :green_circle:", use_aliases=True)

        self.send_message_to_list(snt)