import socket
import sys
import time
import cPickle as pickle
from threading import Thread
from common.message import message
from common.exception import *

MAX_ATTEMPTS = 3
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
    
    def send_sample_message(self):
        self.conn.sendall(pickle.dumps(message.ChatMessage(self.username, "sample text...", self.username)))
        print 'sent sample text to server'

    def logout(self):
        logout_message = message.LogoutMessage()
        b = pickle.dumps(logout_message)
        self.conn.send(b)

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
                flag = chat_message.get_flag()
                '''first check the flags'''
                if flag == 2:
                    reply_from_server = chat_message.get_text()
                    print reply_from_server
                elif flag == -2:
                    print chat_message.get_error_msg()
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
            receiver_username = raw_input("Enter the name of the receiver: ")
            while True:
                text = raw_input().strip()
                chat_message = message.ChatMessage(self.username, text, receiver_username)
                b = pickle.dumps(chat_message)
                self.conn.sendall(b)
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
        
def connect_to_remote_server(conn):
    remote_ip = socket.gethostbyname(HOST)
    for attempt in range(MAX_ATTEMPTS):
        try:
            conn.connect((remote_ip, PORT))
            return True
        except socket.error:
            print 'Could not connect to server. Attempting to reconnect...'
            time.sleep(5)
    raise exception.CouldNotConnectToServerException

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        connect_to_remote_server(conn)
    except exception.CouldNotConnectToServerException as e:
        print e
        sys.exit(1)

    username = get_username_from_client()
    
    ''' create the Client object '''
    client = Client(username, conn)
    
    ''' this is a necessary step '''
    client.send_username_to_server()

    client_as_sender = AsSender(client)
    client_as_sender.start()
    
    client_as_receiver = AsReceiver(client)
    client_as_receiver.start()
    
if __name__ == '__main__': main()