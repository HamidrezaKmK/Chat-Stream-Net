from libtcp import build_server, build_client

main_menu = """1. Connect to external servers
2. Login as admin
3. Exit
"""

app_menu = "shalgham\nchoghondar\n"

clients = {}
firewall_mode = "black"
firewall_rules = {}
admin_pass = "admin"

def check_firewall(port):
    print("checking firewall", firewall_mode, " ", port)
    if firewall_rules.get(port) == None:
        return firewall_mode == "black"
    return firewall_rules[port] == "open"

def connect_to(port, id, callback):
    if not check_firewall(port):
        callback("packet dropped due firewall rules\n")
        return
    def on_exit():
        clients.pop(id)
        callback(main_menu)
    return build_client(callback, on_exit, port)

def handler(message, id, callback):
    global firewall_mode
    global clients
    global firewall_rules
    if clients.get(id) == None:
        if message == "1":
            clients[id] = "user"
            callback(app_menu)
            return
        if message == "2":
            clients[id] = "admin_auth"
            callback("Enter admin password\n")
            return
        if message == "3":
            callback("$special_exit")
            return
        callback(main_menu)
        return
    if clients[id] == "user":
        if message == "shalgham":
            clients[id] = connect_to(10002, id, callback)
            return
        if message == "choghondar":
            clients[id] = connect_to(10003, id, callback)
            return
        if message == "back":
            clients.pop(id)
            callback(main_menu)
            return            
        callback(app_menu)
        return
    if clients[id] == "admin_auth":
        if message == admin_pass:
            callback("Welcome, admin\n")
            clients[id] = "admin"
        else:
            callback("Wrong pass, try again\n")
        return
    if clients[id] == "admin":
        if message == "firewall whitelist activate":
            firewall_mode = "white"
            callback("Done\n")
            return
        if message == "firewall blacklist activate":
            firewall_mode = "black"
            callback("Done\n")
            return
        if message[0:4] == "open":
            firewall_rules[int(message[10:])] = "open"
            callback("Done\n")
            return
        if message[0:5] == "close":
            firewall_rules[int(message[10:])] = "close"
            callback("Done\n")
            return
        if message == "back":
            clients.pop(id)
            callback(main_menu)
            return
        callback("Bad command\n")
        return
        
    clients[id](message)

build_server(handler, 10001, main_menu)
