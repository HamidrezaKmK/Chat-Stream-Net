from libtcp import build_server

main_menu = "Welcome to shalgham\n1. Login\n2. Sign up\n3. Exit\n"

def handler(message, id, callback):
    if message == "1":
        callback("Login not supported\n")
        return
    if message == "2":
        callback("Sign up not supported\n")
        return
    if message == "3":
        callback("$special_exit")
        return
    callback(main_menu)

build_server(handler, 10002, main_menu)
