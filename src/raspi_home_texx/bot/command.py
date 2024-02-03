

class CommandCallback:
    command: str = None
    callback = None

    def __init__(self, command: str, callback):
        self.command = command
        self.callback = callback


class Command:
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

    COMMAND_LIST = {
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

    @staticmethod
    def get_command_list() -> str:
        str_list = ''
        for key, value in list(Command.COMMAND_LIST.items()):
            str_list += key + " - " + value + "\n"

        return str_list
