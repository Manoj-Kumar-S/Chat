from twisted.internet import protocol, reactor
from threading import Thread
import cPickle as pickle
from common.message import message

commands = { 'commands': 'list of available commands. ~commands',
             'help': 'help on how to use a command. ~help <command name>',
             'man': 'same as help. ~man <command name>',
             'exit': 'exit from chatroom. ~exit',
             'ping': 'ping a user. ~ping <user nick>' ,
             'users': 'list of users currently online. ~users',
             'whoami': 'who are you? ~whoami',
             'other': 'who is the user you are chatting with right now. ~other' }

class ChatProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.nick = None
        self.peer = None
        self.current_receiver = None
        self.state = 'REGISTER'
    
    def connectionMade(self):
        self.peer = self.transport.getPeer()
        print 'Client connected from %s:%s' % (self.peer.host, self.peer.port)
        
    def connectionLost(self, reason):
        print '<%s> disconnected at %s:%s' % (self.nick, self.peer.host, self.peer.port)
    
    def dataReceived(self, data):
        if self.state == 'REGISTER':
            self.handle_register(data)
        else:
            self.handle_data(data)
        
    def handle_register(self, nick):
        if nick in self.factory.users:
            '''Create a ServerMessage object to tell that the nick is already in use'''
            server_message = message.ServerMessage('Nick already in use. Try another nick.')
            self.transport.write(pickle.dumps(server_message))
            return
        else:
            self.nick = nick
            self.factory.users[self.nick] = self.transport
            welcome_message = 'Welcome %s! Type ~commands to get the list of available commands.' % (self.nick)
            self.send_server_message(welcome_message)
            self.state = 'CHAT'
        
    def handle_data(self, data):
        '''parse the message object here'''
        text_message = pickle.loads(data)
        '''get the status of the message to see how to handle it'''
        status = text_message.get_status()
        if status == 'COMMAND':
            self.handle_command(text_message)
        elif status == 'CHAT_MESSAGE':
            if self.current_receiver == None:
                self.send_server_message('You need to ping a user before chatting')
                return
            self.handle_chat(text_message)
            
    def handle_command(self, command_message):
        '''command_message is the CommandMessage object'''
        command = command_message.get_command()
        if command not in commands:
            self.send_server_message('Invalid command')
        elif command == 'commands':
            self.send_commands_list()
        elif command == 'help' or command == 'man':
            for_command = command_message.get_tag()
            self.send_help_for_command(for_command)
        elif command == 'users':
            self.send_users_list()
        elif command == 'ping':
            user = command_message.get_tag()
            self.ping_user(user)
        elif command == 'exit':
            self.exit_user()
        elif command == 'whoami':
            self.whoami_user()
        elif command == 'other':
            self.other_user()
            
    def send_commands_list(self):
        result = ''
        for key, value in commands.iteritems():
            result += '%s: %s\n' % (key, value)
        self.send_server_message(result[:len(result) - 1])

    def send_help_for_command(self, command):
        command_info = commands.get(command)
        if command_info is None:
            self.send_server_message('Invalid command name')
        else:
            self.send_server_message(command_info)

    def handle_chat(self, chat_message):
        receiver_transport = self.factory.users.get(self.current_receiver)
        receiver_transport.write(pickle.dumps(chat_message))
            
    def send_users_list(self):
        delimited_users_list = ''
        for user in self.factory.users.keys():
            delimited_users_list += user + ', '
        result = delimited_users_list[0 : len(delimited_users_list)-2]
        self.send_server_message(result)
    
    def ping_user(self, user):
        '''first check if the user is there/online'''
        if user not in self.factory.users.keys():
            self.send_server_message('<%s> is not online right now' % (user))
        else:
            self.send_server_message('You can start chatting with <%s>' % (user))
            self.current_receiver = user

    def whoami_user(self):
        self.send_server_message(self.nick)

    def other_user(self):
        if self.current_receiver is None:
            self.send_server_message('You are not chatting with anyone right now.')
        else:
            self.send_server_message(self.current_receiver)

    def exit_user(self):
        '''Send a message to the current receiver that the user has logged out'''
        if self.current_receiver is not None:
            transport = self.factory.users.get(self.current_receiver)
            if transport is not None:
                self.send_server_message('<%s> has logged out.' % (self.nick), transport)
        self.send_server_message('<%s> has logged out.' % (self.nick), transport)
        self.transport.loseConnection()
        del self.factory.users[self.nick]
    
    def send_server_message(self, text, transport=None):
        server_message = message.ServerMessage(text)
        b = pickle.dumps(server_message)
        if transport is None:
            self.transport.write(b)
            return
        transport.write(b)
    
class ChatFactory(protocol.Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)

reactor.listenTCP(8001, ChatFactory())
print 'Server running, listening for incoming connections...'
reactor.run()