from libtcp import build_server
import socket, cv2, pickle,struct,imutils
import time

client_watching = []

main_menu = "Welcome to choghondar\n1. Teenage Mutant Ninja Turtles\n"
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
        #client_watching.append(id)
        if message == 1:
            path = "TeenageMutantNinjaTurtles.mp4"


        # Socket Create
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host_name  = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        server_socket.bind(('', 0))
        port = server_socket.getsockname()[1]
        print('port:', port)
        socket_address = (host_ip,port)
        
        callback('[{}] {} {}'.format('PORTREQ', port, host_ip))
    
        # Socket Listen
        server_socket.listen(5)
        print("LISTENING AT:", socket_address)

        # Socket Accept
        # Socket Listen
        server_socket.listen(5)
        print("LISTENING AT:",socket_address)

        # Socket Accept
        while True:
            client_socket,addr = server_socket.accept()
            print('GOT CONNECTION FROM:',addr)
            if client_socket:
                vid = cv2.VideoCapture('TomandJerry.mp4')
        
                while(vid.isOpened()):
                    img,frame = vid.read()
                    frame = imutils.resize(frame,width=320)
                    a = pickle.dumps(frame)
                    time.sleep(0.1)
                    message = struct.pack("Q",len(a))+a
                    client_socket.sendall(message)

    callback("$start_udp_and_play_video")

build_server(handler, 10003, main_menu)