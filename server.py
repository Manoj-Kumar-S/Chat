from twisted.internet import protocol, reactor
from threading import Thread
import cPickle as pickle
from common.message import message

commands = ['exit', 'ping', 'users']

class ChatProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.peer = None
        self.current_receiver = None
        self.state = 'REGISTER'
    
    def connectionMade(self):
        self.peer = self.transport.getPeer()
        print 'Client connected from %s:%s' % (self.peer.host, self.peer.port)
        
    def connectionLost(self, reason):
        print '<%s> disconnected at %s:%s' % (self.name, self.peer.host, self.peer.port)
    
    def dataReceived(self, data):
        if self.state == 'REGISTER':
            self.handle_register(data)
        else:
            self.handle_data(data)
        
    def handle_register(self, name):
        if name in self.factory.users:
            '''Create a ServerMessage object to tell that the nick is already in use'''
            server_message = message.ServerMessage('Nick already in use. Try another nick.')
            self.transport.write(pickle.dumps(server_message))
            return
        else:
            self.name = name
            self.factory.users[self.name] = self.transport
            self.state = 'CHAT'
        
    def handle_data(self, chat):
        '''parse the message object here'''
        text_message = pickle.loads(chat)
        '''get the status of the message to see how to handle it'''
        status = text_message.get_status()
        if status == 'COMMAND':
            self.handle_command(text_message)
        elif status == 'CHAT':
            if self.current_receiver == None:
                self.transport.write('* You need to ping a user before you can start chatting *')
                return
            self.handle_chat(text_message)
            
    def handle_command(self, command_message):
        '''command_message is the CommandMessage object'''
        command = command_message.get_command()
        if command not in commands:
            '''create a ServerMessage object here'''
            server_message = message.ServerMessage('Invalid command')
            self.transport.write(pickle.dumps(server_message))
        elif command == 'users':
            self.send_users_list()
        elif command == 'ping':
            user = command_message.get_user()
            self.ping_user(user)
        elif command == 'exit':
            self.exit_user()
            
    def handle_chat(self, text_message):
        transport = self.factory.users.get(self.current_receiver)
        transport.write(pickle.dumps(text_message))
            
    def send_users_list(self):
        delimited_users_list = ''
        for user in self.factory.users.keys():
            delimited_users_list += user + ', '
        result = delimited_users_list[0 : len(delimited_users_list)-2]
        server_message = message.ServerMessage(result)
        self.transport.write(pickle.dumps(server_message))
    
    def ping_user(self, user):
        '''ping user'''
        '''set the current receiver for this user to user'''
        self.current_receiver = user
        server_message = message.ServerMessage('You can start chatting with %s' % (self.current_receiver))
        self.transport.write(pickle.dumps(server_message))

    def exit_user(self):
        self.transport.loseConnection()
        del self.factory.users[self.name]
    
class ChatFactory(protocol.Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)

reactor.listenTCP(8001, ChatFactory())
print 'Server running, listening for incoming connections...'
reactor.run()
    
    
        