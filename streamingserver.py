from libtcp import build_server

main_menu = "Welcome to choghondar\nFilmi nadarim felan\n"

def handler(message, id, callback):
    callback("$start_udp_and_play_video")

build_server(handler, 10003, main_menu)
