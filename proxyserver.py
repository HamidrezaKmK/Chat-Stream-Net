from libtcp import build_client, build_server

clients = {}

def handler(message, id, callback):
    if clients.get(id) == None:
        def on_exit():
            clients.pop(id)
            callback("$special_exit")
        clients[id] = build_client(callback, on_exit, int(message))
        return
    clients[id](message)
print("Enter server port")
build_server(handler, int(input()), "")
