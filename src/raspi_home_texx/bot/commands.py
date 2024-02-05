

class CommandCallback:
    command: str = None
    callback = None

    def __init__(self, command: str, callback):
        self.command = command
        self.callback = callback


class Commands:
    CIAO = "ciao"
    START = "start"
    HELP = "help"
    UPTIME = "uptime"
    TEMPERATURE = "temperature"
    SYSTEM_INFO = "system_info"
    SEND_LOG = "send_log"
    CLEAR_LOG = "clear_log"
    REBOOT = "reboot"
    UPDATE_UPGRADE = "update_upgrade"
    ECU_CHECK = "ecu_check"
    ALARM_CHECK = "alarm_check"
    ECU_TOGGLE = "ecu_toggle"
    ANTI_PANIC = "anti_panic"
    GATE_CHECK = "gate_check"
    GATE_TOGGLE = "gate_toggle"
    GATE_STOP = "gate_stop"

    __descriptions = {
        CIAO: "saluta il bot",
        START: "avvia il bot e lista comandi",
        HELP: "lista dei comandi",
        UPTIME: "tempo totale di avvio",
        TEMPERATURE: "monitor temperatura",
        SYSTEM_INFO: "informazioni di sistema",
        SEND_LOG: "invia il log degli errori/allarmi",
        CLEAR_LOG: "elimina e pulisci il file log",
        REBOOT: "riavvia il bot allarme",
        UPDATE_UPGRADE: "aggiorna il raspi",
        ECU_CHECK: "visualizza lo stato della centralina",
        ALARM_CHECK: "verifica se allarme e' scattato",
        ECU_TOGGLE: "cambia lo stato della centralina",
        ANTI_PANIC: "attiva la funzione antipanico della centralina",
        GATE_CHECK: "verifica lo stato del cancello",
        GATE_TOGGLE: "funzione apertura/chiusura del cancello",
        GATE_STOP: "blocca il cancello"
    }

    def __init__(self, bot_name: str):
        self.__bot_name = bot_name

    def get_command_list(self) -> str:
        str_list = ''
        for key, value in list(self.__descriptions.items()):
            str_list += key + " - " + value + "\n"

        return str_list

    def is_command_in_list(self, command):
        return self.check_command_equality(command, self.CIAO) or \
            self.check_command_equality(command, self.START) or \
            self.check_command_equality(command, self.HELP) or \
            self.check_command_equality(command, self.UPTIME) or \
            self.check_command_equality(command, self.TEMPERATURE) or \
            self.check_command_equality(command, self.SYSTEM_INFO) or \
            self.check_command_equality(command, self.SEND_LOG) or \
            self.check_command_equality(command, self.CLEAR_LOG) or \
            self.check_command_equality(command, self.REBOOT) or \
            self.check_command_equality(command, self.UPDATE_UPGRADE) or \
            self.check_command_equality(command, self.ECU_CHECK) or \
            self.check_command_equality(command, self.ALARM_CHECK) or \
            self.check_command_equality(command, self.ECU_TOGGLE) or \
            self.check_command_equality(command, self.ANTI_PANIC) or \
            self.check_command_equality(command, self.GATE_CHECK) or \
            self.check_command_equality(command, self.GATE_TOGGLE) or \
            self.check_command_equality(command, self.GATE_STOP)

    def check_command_equality(self, command_rcv, command_name):
        return command_rcv == command_name or command_rcv == self.__full_command_name(command_name)

    def __full_command_name(self, cmd):
        return cmd + "@" + self.__bot_name
