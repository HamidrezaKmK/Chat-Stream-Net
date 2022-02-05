from libtcp import build_server, build_client

main_menu = """1. Connect to external servers
2. Login as admin
3. Exit
"""

app_menu = "shalgham\nchoghondar\n"

clients = {}

def connect_to(port, id, callback):
    def on_exit():
        clients.pop(id)
        callback(main_menu)
    return build_client(callback, on_exit, port)

def handler(message, id, callback):
    if clients.get(id) == None:
        if message == "1":
            clients[id] = "1"
            callback(app_menu)
            return
        if message == "3":
            callback("$special_exit")
            return
        callback(main_menu)
        return
    if clients[id] == "1":
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
    clients[id](message)

build_server(handler, 10001, main_menu)
