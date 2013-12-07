"""Defines all Exception classes"""

class UserNotOnlineException(Exception, ):
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