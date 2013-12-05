''' this defines the Basic class '''

''' this in an abstract class extended by all the communication classes (eg. Message) '''

''' the flag member is used to differentiate between the various types of communication that 
    can be possible between the client and the server '''

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