from libtcp import build_server
import socket, cv2, pickle,struct,imutils

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

        print('HOST IP:',host_ip)
        socket_address = (host_ip, port)

        # Socket Bind
#server_socket.bind(socket_address)

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
                vid = cv2.VideoCapture('TeenageMutantNinjaTurtles.mp4')
        
                while(vid.isOpened()):
                    img,frame = vid.read()
                    frame = imutils.resize(frame,width=320)
                    a = pickle.dumps(frame)
                    message = struct.pack("Q",len(a))+a
                    client_socket.sendall(message)
            
                    cv2.imshow('TRANSMITTING VIDEO',frame)
                    if cv2.waitKey(1) == '13':
                        client_socket.close()

    callback("$start_udp_and_play_video")

build_server(handler, 10003, main_menu)