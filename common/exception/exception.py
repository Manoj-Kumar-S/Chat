"""Defines all Exception classes"""
from common.message import message

class UserNotOnlineException(Exception, message.Basic):
    """Raise this when a particular user is not online"""
    def __init__(self):
        self.__error_msg = "Sorry, the requested user is not online right now. Please try again later."
        self._flag = -2

    def __str__(self):
        return self.__error_msg
    
    def get_error_msg(self):
        return self.__error_msg

    def get_flag(self):
        return self._flag

class CouldNotConnectToServerException(Exception):
    """Raise this when the client connect to the server"""
    def __init__(self):
        self.__error_msg = "Fatal Error: Could not connect to the server. Please try again later."
    
    def __str__(self):
        return self.__error_msg

    def get_error_msg(self):
        return self.__error_msg