import socket
import sys
import cPickle as pickle
from threading import Thread
from common.message import message

''' host address and port of the server on which to connect '''
HOST = 'localhost'
PORT = 8888

class Client(object):
    """Chat client"""
    def __init__(self, username, conn):
        self.username = username
        self.conn = conn

    def send_username_to_server(self):
        """Send the username of the client to the server."""
        u_message = message.UsernameMessage(self.username)
        b = pickle.dumps(u_message)
        self.conn.sendall(b)

class AsReceiver(Thread):
    """This class handles all the incoming chats for the client."""
    def __init__(self, client):
        Thread.__init__(self)
        self.username = client.username
        self.conn = client.conn
    def run(self):
        try:
            while True:
                data = self.conn.recv(1024)
                chat_message = pickle.loads(data)
                reply_from_server = chat_message.get_text()
                print reply_from_server
        except AttributeError:
            print "Error: The unpickled object does not allow the requested operation"    
            
class AsSender(Thread):
    """This class handles all the outgoing chats for the client."""
    def __init__(self, client):
        Thread.__init__(self)
        self.username = client.username
        self.conn= client.conn
    def run(self):
        try:
            text = raw_input("Enter message and press <return> to send it to the server\n")
            while True:
                chat_message = message.ChatMessage(self.username, text, self.username)
                b = pickle.dumps(chat_message)
                self.conn.sendall(b)
                text = raw_input().strip()
        except AttributeError:
            print "Error: The unpickled object does not allow the requested operation"

def get_username_from_client():
    """Get the username from the client."""
    name = raw_input("Enter a username: ").strip()
    while(True):
        if name is "":
            name = raw_input("Invalid username, please try again: ").strip()
        else:
            return name

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_ip = socket.gethostbyname(HOST)
    conn.connect((remote_ip, PORT))
    username = get_username_from_client()
    
    ''' create the Client object '''
    client = Client(username, conn)
    
    ''' this is a necessary step '''
    client.send_username_to_server()
    
    ''' start the outgoing chat thread for the client. '''
    client_as_sender = AsSender(client)
    client_as_sender.start()
    
    ''' start the incoming chat thread for the client. '''
    client_as_receiver = AsReceiver(client)
    client_as_receiver.start()

if __name__ == '__main__': main()