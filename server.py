import socket
import cPickle as pickle
from threading import Thread

HOST = ''
PORT = 8888
list_of_users = []

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
        print 'Server set up, listening for incoming connections'
        
    def tear_down(self):
        """Abort the server."""
        ''' also abort all the client connections '''
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
        self.addr = client[1]
        ''' self.addr is the tuple of IP and port of the client '''
        
        ''' the username of the client handled by this thread '''
        self.client_username = "anon"

    def run(self):

        def parse_user_response(data):
            """Parse reply from the client."""

            def parse_response_for_username(username_message):
                """Parse response from the client for the username."""
                self.client_username = username_message.get_username()
                print 'client username: ' + self.client_username
                list_of_users.append(self.client_username)

            def parse_response_for_chat(chat_message):
                """Parse response from the client for the chat message."""
                print 'chat message: ' + chat_message.get_text()
                print 'chat sender: ' + chat_message.get_sender()
                print 'chat_receiver: ' + chat_message.get_receiver()

            basic_object = pickle.loads(data)
            ''' get the flag from the unpickled object and handle it appropriately '''
            flag = basic_object.get_flag()
            if flag == 1:
                parse_response_for_username(basic_object)
            elif flag == 2:
                parse_response_for_chat(basic_object)

        data = self.conn.recv(1024)
        parse_user_response(data)

def main():
    server = Server()
    server.set_up()
    server.run()
if __name__ == '__main__': main()