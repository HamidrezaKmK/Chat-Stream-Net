from libtcp import build_server
import socket

client_watching = []

main_menu = "Welcome to choghondar\nFilmi nadarim felan\n"
path = ""

def handler(message, id, callback):
    if id in client_watching:
        if message == "/exit":
            client_watching.remove(id)
    else:
        try:
            message = int(message)
        except ValueError:
            callback("not a number!")
        client_watching.append(id)
        if message == 1:
            path = "TeenageMutantNinjaTurtles.mp4"

        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#sock = socket.socket()
        server_socket.bind(('', 0))
        port = server_socket.getsockname()[1]

        host_name  = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
    
    
        callback('[{}] {} {}'.format('PORTREQ', port, host_ip))

    callback("$start_udp_and_play_video")

build_server(handler, 10003, main_menu)