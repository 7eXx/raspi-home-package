from typing import List, Optional, Union

from .. import get_console_logger, file_logger
from telegram import Message, User

from telegram.ext import MessageFilter
from telegram.ext.filters import DataDict


class ChatFilter(MessageFilter):
    __logger = None
    __list_id = None

    def __init__(self, list_id: List[int]):
        super(self.__class__, self).__init__()
        self.__logger = get_console_logger(self.__class__.__name__)
        self.__list_id = list_id

    def filter(self, message: Message) -> Optional[Union[bool, DataDict]]:
        if self.__user_is_authorized(message.from_user):
            return True
        else:
            self.__log_user_unauthorized(message.from_user)
            return False

    def __user_is_authorized(self, user: User):
        return user.id in self.__list_id

    def __log_user_unauthorized(self, user: User):
        if user.username is None:
            self.__log_first_name(user)
        else:
            self.__log_username(user)

    def __log_first_name(self, user: User):
        self.__logger.warning("XX Access Denied for this bot XX, "
                              "user first name: " + user.first_name + ", your chat id: " + str(user.id))
        file_logger.write(
            "access denied from: first_name {0}, chat_id {1}".format(user.first_name, str(user.id)))

    def __log_username(self, user: User):
        self.__logger.warning("XX Access Denied for this bot XX "
                              "your username: " + user.username + ", your chat id: " + str(user.id))
        file_logger.write(
            "acced denied from: username {0}, chat_id {1}".format(user.username, str(user.id)))
