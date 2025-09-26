from abc import ABC
from typing import Callable, Dict


class _BaseCallback(ABC):
    _literal: str = None
    _callback: Callable = None

    def __init__(self, literal: str, callback: Callable):
        self._literal = literal
        self._callback = callback

    def get_callback(self):
        return self._callback


class CommandCallback(_BaseCallback):

    def __init__(self, command: str, callback: Callable):
        super().__init__(command, callback)

    def get_commands(self):
        return self._literal


class MessageCallback(_BaseCallback):

    def __init__(self, message: str, callback: Callable,):
        super().__init__(message, callback)

    def get_message(self):
        return self._literal


class Commands:
    CIAO = "ciao"
    START = "start"
    HELP = "help"
    UPTIME = "uptime"
    SEND_LOG = "send_log"
    CLEAR_LOG = "clear_log"
    TEMPERATURE = "temperature"
    SYSTEM_INFO = "system_info"
    ECU_CHECK = "ecu_check"
    ALARM_CHECK = "alarm_check"
    ECU_TOGGLE = "ecu_toggle"
    ANTI_PANIC = "anti_panic"
    GATE_CHECK = "gate_check"
    GATE_TOGGLE = "gate_toggle"
    GATE_STOP = "gate_stop"

    _descriptions: Dict[str, str] = {}

    def __init__(self, bot_name: str):
        self.__bot_name = bot_name
        self._descriptions = {
            Commands.CIAO: "saluta il bot",
            Commands.START: "avvia il bot e lista comandi",
            Commands.HELP: "lista dei comandi",
            Commands.UPTIME: "tempo totale di avvio",
            Commands.SEND_LOG: "invia il log degli errori/allarmi",
            Commands.CLEAR_LOG: "elimina e pulisci il file log",
            Commands.TEMPERATURE: "monitor temperatura",
            Commands.SYSTEM_INFO: "informazioni di sistema",
            Commands.ECU_CHECK: "visualizza lo stato della centralina",
            Commands.ALARM_CHECK: "verifica se allarme e' scattato",
            Commands.ECU_TOGGLE: "cambia lo stato della centralina",
            Commands.ANTI_PANIC: "attiva la funzione antipanico della centralina",
            Commands.GATE_CHECK: "verifica lo stato del cancello",
            Commands.GATE_TOGGLE: "funzione apertura/chiusura del cancello",
            Commands.GATE_STOP: "blocca il cancello",
        }

    def _add_command(self, command: str, description: str):
        self._descriptions[command] = description

    def get_command_list(self) -> str:
        str_list = ''
        for key, value in list(self._descriptions.items()):
            str_list += key + " - " + value + "\n"

        return str_list

    def is_command_in_list(self, command):
        for key, value in list(self._descriptions.items()):
            if self.check_command_equality(command, key):
                return True

        return False

    def check_command_equality(self, command_rcv, command_name):
        return command_rcv == command_name or command_rcv == self.__full_command_name(command_name)

    def __full_command_name(self, cmd):
        return cmd + "@" + self.__bot_name
