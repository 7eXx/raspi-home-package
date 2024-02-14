import unittest

from src.raspi_home_texx.bot.commands import Commands


class CommandsExtended(Commands):

    UPDATE_UPGRADE = "update_upgrade"

    def __init__(self, bot_name: str):
        super().__init__(bot_name)
        self._add_command(self.UPDATE_UPGRADE, "Aggiorna il sistema")


class TestCommands(unittest.TestCase):

    def setUp(self):
        self.commands = Commands("Bot_name")
        self.commands_extended = CommandsExtended("Bot_name")

    def test_is_command_in_list(self):
        self.assertTrue(self.commands.is_command_in_list("gate_toggle"))
        self.assertTrue(self.commands.is_command_in_list("anti_panic"))
        self.assertTrue(self.commands.is_command_in_list("system_info"))

        self.assertFalse(self.commands.is_command_in_list("update_upgrade"))

    def test_is_command_in_list_extended(self):
        self.assertTrue(self.commands_extended.is_command_in_list("gate_toggle"))
        self.assertTrue(self.commands_extended.is_command_in_list("anti_panic"))
        self.assertTrue(self.commands_extended.is_command_in_list("system_info"))

        self.assertTrue(self.commands_extended.is_command_in_list("update_upgrade"))


