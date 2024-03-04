from typing import Callable, Dict


class CommandCallback:
    command: str = None
    callback: Callable = None

    def __init__(self, command: str, callback: Callable):
        self.command = command
        self. callback = callback


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
            self.CIAO: "saluta il bot",
            self.START: "avvia il bot e lista comandi",
            self.HELP: "lista dei comandi",
            self.UPTIME: "tempo totale di avvio",
            self.SEND_LOG: "invia il log degli errori/allarmi",
            self.CLEAR_LOG: "elimina e pulisci il file log",
            self.TEMPERATURE: "monitor temperatura",
            self.SYSTEM_INFO: "informazioni di sistema",
            self.ECU_CHECK: "visualizza lo stato della centralina",
            self.ALARM_CHECK: "verifica se allarme e' scattato",
            self.ECU_TOGGLE: "cambia lo stato della centralina",
            self.ANTI_PANIC: "attiva la funzione antipanico della centralina",
            self.GATE_CHECK: "verifica lo stato del cancello",
            self.GATE_TOGGLE: "funzione apertura/chiusura del cancello",
            self.GATE_STOP: "blocca il cancello",
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
