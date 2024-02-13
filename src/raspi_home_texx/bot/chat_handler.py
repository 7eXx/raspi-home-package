import subprocess
import emoji
import time

from telegram import Update
from telegram.ext import CallbackContext
from .. import get_console_logger, file_logger
from .commands import Commands
from ..automation import Automation


class ChatHandler:
    _commands = None
    _automation = None
    _logger = None

    def __init__(self, commands: Commands, automation: Automation):
        self._commands = commands
        self._automation = automation
        self._logger = get_console_logger(self.__class__.__name__)

    def ciao(self, update: Update, context: CallbackContext):
        self._logger.info("ricevuto il saluto")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hey ciao, attendo un comando. Usa /help per la lista")

    def start(self, update: Update, context: CallbackContext):
        self._logger.info("lista comandi per start")
        context.bot.send_message(chat_id=update.effective_chat.id, text=self._commands.get_command_list())

    def help(self, update: Update, context: CallbackContext):
        self._logger.info("lista comandi per help")
        context.bot.send_message(chat_id=update.effective_chat.id, text=self._commands.get_command_list())

    def uptime(self, update: Update, context: CallbackContext):
        self._logger.info("informazioni uptime")
        out_mess = subprocess.getoutput("uptime")
        context.bot.send_message(chat_id=update.effective_chat.id, text=out_mess)

    def send_log(self, update: Update, context: CallbackContext):
        self._logger.info('invio file di log')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=emoji.emojize("Ti sto inviando il file di log :memo:", use_aliases=True))
        if file_logger.is_log_exists():
            context.bot.send_document(chat_id=update.effective_chat.id,
                                      document=open(file_logger.get_file_path(), 'rb'))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emoji.emojize("Non ci sono file di log :mag:", use_aliases=True))

    def clear_log(self, update: Update, context: CallbackContext):
        self._logger.info("eliminazione file log")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=emoji.emojize("Pulizia del file log :floppy_disk:", use_aliases=True))
        file_logger.delete_if_log_exists()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=emoji.emojize("File log eliminato :wrench:", use_aliases=True))

    def reboot(self, update: Update, context: CallbackContext):
        self._logger.info('sto per riavviare')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=emoji.emojize('sto riavviando :zzz:', use_aliases=True))
        time.sleep(5)
        subprocess.call("sudo reboot", shell=True)

    def update_upgrade(self, update: Update, context: CallbackContext):
        self._logger.info("sto per aggiornare il sistema")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Sto aggiornando le dipendenze')
        subprocess.call("sudo apt-get update", shell=True)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Sto aggiornando i pacchetti')
        subprocess.call("sudo apt-get upgrade -y", shell=True)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Sto rimuovendo i pacchetti inutilizzati')
        subprocess.call("sudo apt-get autoremove -y", shell=True)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Aggiornamento concluso')

    def temperature_cpu(self, update: Update, context: CallbackContext):
        self._logger.info('ti dico la temperatura')
        temperature, unit = self._automation.temperature()
        str_temperature = str(temperature) + " " + unit
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=(emoji.emojize('temperatura :warning:: ', use_aliases=True)) + str_temperature)

    def system_info(self, update: Update, context: CallbackContext):
        self._logger.info('Ti dico le informazioni di sistema')
        pretty_sys_info = self._automation.system_info().format_pretty()
        context.bot.send_message(chat_id=update.effective_chat.id, text=pretty_sys_info)

    def ecu_check(self, update: Update, context: CallbackContext):
        self._logger.info("verifico lo stato della centralina")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=emoji.emojize("verifico lo stato della centralina :house:", use_aliases=True))

        if self._automation.is_alarm_ecu_active():
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emoji.emojize("Centralina armata :bell:", use_aliases=True))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emoji.emojize("Centralina spenta :no_bell:", use_aliases=True))

    def alarm_check(self, update: Update, context: CallbackContext):
        self._logger.info("verifico lo stato dell'allarme ")
        context.bot.sendMessage(chat_id=update.effective_chat.id,
                                text=emoji.emojize("verifico lo stato dell'allarme :warning:", use_aliases=True))

        if self._automation.is_alarm_ringing():
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emoji.emojize("allarme sta suonando :rotating_light:", use_aliases=True))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emoji.emojize("allarme in regola :green_heart:", use_aliases=True))

    def ecu_toggle(self, update: Update, context: CallbackContext):
        self._logger.info("sto cambiando lo stato della centralina")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=emoji.emojize("cambio lo stato della centralina :house:", use_aliases=True))

        prev_state = self._automation.is_alarm_ecu_active()
        new_state = self._automation.toggle_alarm_ecu()

        if self._automation.is_alarm_ecu_test_mode(prev_state, new_state):
            msg = "tests mode off"
            to_send = emoji.emojize(msg + " :no_bell:", use_aliases=True)
        else:
            if new_state:
                msg = "centralina armata"
                to_send = emoji.emojize(msg + " :bell:", use_aliases=True)
            else:
                msg = "centralina spenta"
                to_send = emoji.emojize(msg + " :no_bell:", use_aliases=True)

        self._logger.debug(msg)
        file_logger.write(msg)
        context.bot.send_message(chat_id=update.effective_chat.id, text=to_send)

    def anti_panic(self, update: Update, context: CallbackContext):
        self._logger.info("sto cambiando lo stato della centralina")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=emoji.emojize("comando antipanico inviato :purple_heart:", use_aliases=True))

        self._automation.anti_panic_mode()

    def gate_check(self, update: Update, context: CallbackContext):
        self._logger.info("verifico lo stato del cancello")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=emoji.emojize("verifico lo stato del cancello :door:", use_aliases=True))

        if self._automation.is_gate_open():
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emoji.emojize("Cancello aperto :unlock:", use_aliases=True))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emoji.emojize("Cancello chiuso :lock:", use_aliases=True))

    def gate_toggle(self, update: Update, context: CallbackContext):
        self._logger.info("sto aprendo/chiudendo il cancello")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=emoji.emojize("sto aprendo/chiudendo il cancello :door:", use_aliases=True))

        if self._automation.toggle_gate_ecu():
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emoji.emojize("Cancello aperto :unlock:", use_aliases=True))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emoji.emojize("Cancello chiuso :lock:", use_aliases=True))

    def gate_stop(self, update: Update, context: CallbackContext):
        self._logger.info("sto fermando il cancello")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=emoji.emojize("sto fermando il cancello :door:", use_aliases=True))

        if self._automation.stop_gate():
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emoji.emojize("Cancello aperto :unlock:", use_aliases=True))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emoji.emojize("Cancello chiuso :lock:", use_aliases=True))