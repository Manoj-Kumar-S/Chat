import socket
import cPickle as pickle
from threading import Thread
from common.message import message
from common.exception.exception import *

HOST = ''
PORT = 8888

'''dictionary to map a username to its connection to the server'''
list_of_users = {}

def print_all_users():
    """Print the current list of users."""
    for user in list_of_users:
        print user

class Server():
    """Chat Server"""
    def __init__(self):
        self.s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_up(self):
        """Set up the server."""
        self.s_socket.bind((HOST, PORT))
        self.s_socket.listen(10)
        print 'Server set up, listening for incoming connections...\n'
        
    def tear_down(self):
        """Abort the server."""
        
        '''close all existing connections'''
        for conn in list_of_users.itervalues(): conn.close()
        del list_of_users
        self.s_socket.close()

    def run(self):
        """Run the server."""
        while(True):
            client = self.s_socket.accept()
            ''' client is the tuple of the socket connection and the address of the client '''
            print 'Client connected from ' + client[1][0] + ':' + str(client[1][1])
            client_thread = ServiceThread(client)
            client_thread.start()

class ServiceThread(Thread):
    """Thread to service a given client."""
    def __init__(self, (client)):
        Thread.__init__(self)
        self.conn = client[0]
        ''' self.addr is the tuple of IP and port of the client '''
        self.addr = client[1]
    def run(self):
        def parse_user_response(data):
            """Parse reply from the client."""
            def parse_response_for_username(username_message):
                """Parse response from the client for the username."""
                self.client_username = username_message.get_username()
                print 'username: ' + self.client_username
                print '-------------------------------------'
                list_of_users[self.client_username] = self.conn

            def parse_response_for_chat(chat_message):
                """Parse response from the client for the chat message."""
                text_from_client = chat_message.get_text()
                receiver_of_text = chat_message.get_receiver()
                
                if not list_of_users.has_key(receiver_of_text):
                    raise UserNotOnlineException
                ''' before this check if the receiver is online or not. if not, respond to the client '''
                chat_reply = message.ChatMessage(self.client_username, text_from_client, receiver_of_text)
                b = pickle.dumps(chat_reply)
                list_of_users.get(receiver_of_text).sendall(b)

            basic_object = pickle.loads(data)
            ''' get the flag from the unpickled object and handle it appropriately '''
            try:
                flag = basic_object.get_flag()
            except AttributeError:
                raise
            try:
                if flag == 1:
                    parse_response_for_username(basic_object)
                elif flag == 2:
                    parse_response_for_chat(basic_object)
            except UserNotOnlineException:
                raise
        try:
            while True:
                data = self.conn.recv(1024)
                parse_user_response(data)
        except (EOFError, socket.error):
            print "The client has logged out or the connection has been disconnected."
        except AttributeError:
            print "The unpickled object does not allow the requested operation."
        except UserNotOnlineException as e:
            '''send the exception message to the client'''
            b = pickle.dumps(e)
            self.conn.sendall(b)

def main():
    server = Server()
    server.set_up()
    server.run()

if __name__ == '__main__': main()