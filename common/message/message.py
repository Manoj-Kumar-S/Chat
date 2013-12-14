"""Contains the Basic, UsernameMessage and the ChatMessage classes used for communication between client and server."""

class Basic(object):
    def __init__(self):
        pass

    def get_status(self):
        raise NotImplementedError
    
class ChatMessage(Basic):
    def __init__(self, sender, text, receiver=None):
        self._sender = sender
        self._text = text
        self._receiver = receiver
        self._status = 'CHAT'

    def get_sender(self):
        return self._sender

    def get_receiver(self):
        return self._receiver
    
    def get_text(self):
        return self._text
    
    def get_status(self):
        return self._status
    
class CommandMessage(Basic):
    def __init__(self, command, tag=None):
        self._command = command
        self._status = 'COMMAND'
        self._tag = tag

    def get_command(self):
        return self._command
    
    def get_tag(self):
        return self._tag

    def get_status(self):
        return self._status
    
'''a message that the server sends to the client'''
class ServerMessage(Basic):
    def __init__(self, text):
        self._text = text
        self._status = 'SERVER_MESSAGE'
    
    def get_text(self):
        return self._text

    def get_status(self):
        return self._status