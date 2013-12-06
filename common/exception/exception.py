"""Defines all Exception classes"""

class UserNotOnlineException(Exception):
    """Raise this when a particular user is not online"""
    def __init__(self):
        self.__error_msg = "Sorry, the requested user is currently not online. Please try again later."
    
    def __str__(self):
        return self.__error_msg