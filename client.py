import socket
import cPickle as pickle
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
        print 'sent the username to the server'
        
    def send_sample_chat_to_server(self):
        """Send a sample chat message to the server."""
        text = "this is just some sample text..."
        sender = self.username
        receiver = self.username
        chat_message = message.ChatMessage(sender, text, receiver)
        b = pickle.dumps(chat_message)
        self.conn.sendall(b)

def get_username_from_client():
    """Get the username from the client."""
    name = raw_input("Enter a username: ")
    while(True):
        if name.strip() is "":
            name = raw_input("Invalid username, please try again: ")
        else:
            return name.strip()

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_ip = socket.gethostbyname(HOST)
    conn.connect((remote_ip, PORT))
    username = get_username_from_client()
    
    ''' create the Client object '''
    client = Client(username, conn)
    client.send_username_to_server()

if __name__ == '__main__': main()