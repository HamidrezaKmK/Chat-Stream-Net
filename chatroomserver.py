from libtcp import build_server
import json
import jsonpickle
from json import JSONEncoder

main_menu = "Welcome to shalgham\n1. Sign up\n2. Login\n3. Exit\n"


class Message:
    def __init__(self, sender, receiver, text, read_unread=False):
        self.sender = sender
        self.receiver = receiver
        self.text = text
        self.read_unread = read_unread


class User:
    all_user_pass = dict()

    @staticmethod
    def save_users():
        with open('data/chatroomUsers.json', 'w') as out_file:
            empJson = jsonpickle.encode(User.all_user_pass, unpicklable=False)
            out_file.write(json.dumps(empJson, indent=4))

    def __init__(self, username, password, current_session=None):
        self.username = username
        self.password = password
        self.current_session = current_session
        User.all_user_pass[username] = self
        self.inbox = {}
        self.current_state = 'offline'

        User.save_users()

    # def toJson(self):
    #     return json.dumps(self, default=lambda o: o.__dict__)


    def set_state(self, state):
        self.current_state = state

    def set_session(self, session):
        self.current_session = session

    def enter_chat(self, username):
        if username not in User.all_user_pass.keys():
            raise "chattee with name {} not available!".format(username)
        self.chattee = username
        self.set_state('online-direct')
        if username not in self.inbox.keys():
            self.inbox[username] = []

    def inbox_print(self):
        inbox_msg = []
        for name, message_list in self.inbox.items():
            cnt = 0
            for message in message_list:
                if message.sender != self.username and not message.read_unread:
                    cnt += 1
            ch = name
            if cnt > 0:
                ch = '{} ({})'.format(name, cnt)
            inbox_msg.append(ch)
        ret = 'inbox empty!\nUse -send-direct to send a new message\n' if len(inbox_msg) == 0 else '\n'.join(inbox_msg) + '\n'
        ret = '---------------------------\n-----------inbox-----------\n---------------------------\n' + ret
        return ret
    @staticmethod
    def check_username_redundant(username):
        return username in User.all_user_pass.keys()


# A mapping from client ids to users
logged_in_clients = {}
signing_up_clients = {}
logging_in_clients = {}


def chat_guide(username):
    ret = "Chatting with {}".format(username)
    ret += "\nPress /exit to exit chat"
    ret += "\nPress /load x to load the last (x) messages"
    ret += "\nEnter anything not starting with / to send to the user\n"
    return ret


def handle_user_message(message, user, callback):
    if user.current_state == 'online-inbox':
        # callback("receiving message in the inbox state!")
        message = message.strip()
        if message[:12] == '-send-direct':
            username = message.split()[-1]
            if User.check_username_redundant(username):
                if username == user.username:
                    callback("Can't send message to yourself!")
                else:
                    callback(chat_guide(username))
                    user.enter_chat(username)
            else:
                callback("Username non-existant in server!")
        else:
            username = message
            if username in user.inbox.keys():
                callback(chat_guide(username))
                user.enter_chat(username)
            else:
                callback("{} is not available in your inbox!\n"
                         "try \"-send-direct (username)\" to chat with someone with no history")
    elif user.current_state == 'online-direct':
        message = message.strip()
        if message == '/exit':
            callback(user.inbox_print())
            user.set_state('online-inbox')
        elif message[:5] == '/load':
            num = int(message.strip().split()[-1])
            if user.chattee in user.inbox.keys():
                message_list = user.inbox[user.chattee]
                lst_messages = message_list[max(0, len(message_list) - num):]
                ret = chat_guide(user.chattee)
                for msg in lst_messages:
                    if msg.sender != user.username:
                        ret += '({}) {}\n'.format(msg.sender, msg.text)
                        msg.read_unread = True
                    else:
                        ret += msg.text + '\n'
                callback(ret)
            else:
                callback("No chat history to load!")
        else:
            msg = Message(sender=user.username, receiver=user.chattee, text=message)
            user.inbox[user.chattee].append(msg)
            # TODO: if the person is online and in the chat place then it should pop up for them and the message itself should be considered read
            chattee_user = User.all_user_pass[user.chattee]
            if user.username not in chattee_user.inbox:
                chattee_user.inbox[user.username] = []
            chattee_user.inbox[user.username].append(msg)

            User.save_users()


def handler(message, id, callback):
    if id in logged_in_clients.keys():
        handle_user_message(message, logged_in_clients[id], callback)
    elif id in signing_up_clients.keys():
        if signing_up_clients[id] == 'username-req':
            username = message.strip()
            if not User.check_username_redundant(username):
                callback("Please enter your password")
                signing_up_clients[id] = 'password-req--{}'.format(username)
            else:
                callback("This username is already existed or invalid. Please enter another one.")
        elif signing_up_clients[id][:12] == 'password-req':
            password = message.strip()
            username = signing_up_clients[id][14:]
            user = User(username, password, id)
            logged_in_clients[id] = user
            callback(logged_in_clients[id].inbox_print())
            logged_in_clients[id].set_state('online-inbox')
        else:
            raise "Undefined state for user who is signing-up."
    elif id in logging_in_clients.keys():
        if logging_in_clients[id] == 'username-req':
            username = message.strip()
            if User.check_username_redundant(username):
                callback("Please enter your password")
                logging_in_clients[id] = 'password-req--{}'.format(username)
            else:
                callback("The username does not exist! Enter another one ...")
        elif logging_in_clients[id][:12] == 'password-req':
            password_input = message.strip()
            username = logging_in_clients[id][14:]
            print(User.all_user_pass[username])
            print(type(User.all_user_pass[username]))
            if User.all_user_pass[username].password == password_input:
                logged_in_clients[id] = User.all_user_pass[username]
                logged_in_clients[id].set_session(id)
                callback(logged_in_clients[id].inbox_print())
                logged_in_clients[id].set_state('online-inbox')
            else:
                callback("Password does not match with the username! Please re-enter ...")
        else:
            raise "Undefined state for user who is logging in."
    else:
        if message == "1":
            # Sign up
            callback("Please enter your username:")
            signing_up_clients[id] = 'username-req'
            return
        if message == "2":
            # Login
            callback("Please enter your username:")
            logging_in_clients[id] = 'username-req'
            return
        if message == "3":
            callback("$special_exit")
            return

print("Loading chatroom server files...")
try:
    with open('data/chatroomUsers.json', 'r') as in_file:
        tt = in_file.read()
        tt = jsonpickle.decode(tt)
        User.all_user_pass = json.loads(tt)
        for key, user_dict in User.all_user_pass.items():
            user = User(user_dict['username'], user_dict['password'])
            user.current_state = user_dict['current_state']
            user.inbox = {}
            for sender, msg_list in user_dict['inbox'].items():
                user.inbox[sender] = []
                for msg in msg_list:
                    user.inbox[sender].append(Message(msg['sender'], msg['receiver'], msg['text'], msg['read_unread']))
            if 'chattee' in user_dict.keys():
                user.chattee = user_dict['chattee']
            User.all_user_pass[key] = user

except FileNotFoundError:
    pass

build_server(handler, 10002, main_menu)
