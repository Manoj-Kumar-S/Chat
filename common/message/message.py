"""Contains the Basic, UsernameMessage and the ChatMessage classes used for communication between client and server."""

class Basic(object):
    def __init__(self):
        pass

    def get_flag(self):
        raise NotImplementedError
    
class UsernameMessage(Basic):
    def __init__(self, username):
        self._username = username
        self._flag = 1
        
    def get_username(self):
        return self._username

    def get_flag(self):
        return self._flag
    
class ChatMessage(Basic):
    def __init__(self, sender, text, receiver):
        self._sender = sender
        self._text = text
        self._receiver = receiver
        self._flag = 2

    def get_sender(self):
        return self._sender
    
    def get_receiver(self):
        return self._receiver
    
    def get_text(self):
        return self._text
    
    def get_flag(self):
        return self._flag

class ReceiverUsernameMessage(Basic):
    def __init__(self, receiver_username):
        self.__receiver_username = receiver_username
        self._flag = 3
    def get_receiver_username(self):
        return self.__receiver_username
    
    def get_flag(self):
        return self._flag