from abc import ABC

from ..automation import Automation
from telegram import Update
from telegram.ext import CallbackContext


class ChatHandler(ABC):

    def __init__(self, automation: Automation):
        self.__automation = automation

    def ciao(self, update: Update, context: CallbackContext):
        pass

    def start(self, update: Update, context: CallbackContext):
        pass

    def help(self, update: Update, context: CallbackContext):
        pass

    def uptime(self, update: Update, context: CallbackContext):
        pass

    def temperature_cpu(self, update: Update, context: CallbackContext):
        pass

    def system_info(self, update: Update, context: CallbackContext):
        pass

    def send_log(self, update: Update, context: CallbackContext):
        pass

    def clear_log(self, update: Update, context: CallbackContext):
        pass

    def reboot(self, update: Update, context: CallbackContext):
        pass

    def update_upgrade(self, update: Update, context: CallbackContext):
        pass

    def ecu_check(self, update: Update, context: CallbackContext):
        pass

    def alarm_check(self, update: Update, context: CallbackContext):
        pass

    def ecu_toggle(self, update: Update, context: CallbackContext):
        pass

    def anti_panic(self, update: Update, context: CallbackContext):
        pass

    def gate_check(self, update: Update, context: CallbackContext):
        pass

    def gate_toggle(self, update: Update, context: CallbackContext):
        pass

    def gate_stop(self, update: Update, context: CallbackContext):
        pass