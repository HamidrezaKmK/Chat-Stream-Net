from libtcp import build_server
import socket, cv2, pickle,struct,imutils
import time, os

client_watching = []
movies_list = []

directory = os.fsencode("videos")
counter = 0

main_menu = "Welcome to choghondar\n"
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".mp4"):
        counter = counter + 1
        #print(counter, end = '. ')
        #print(filename.replace('.mp4', ''))
        main_menu = main_menu + str(counter) + '. ' + filename.replace('.mp4', '') + '\n'
        movies_list.append(filename)
    else:
        continue

#main_menu = "Welcome to choghondar\n1. Teenage Mutant Ninja Turtles\n"
print(main_menu)

def handler(message, id, callback):
    if message == "back":
        callback("$special_exit")
        return
    if id in client_watching:
        if message == "/exit":
            client_watching.remove(id)
    else:
        try:
            message = int(message)
        except ValueError:
            callback("not a number!")
        #client_watching.append(id)
        path = "videos/"
        path = path + str(movies_list[message - 1])
        print(path)


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
                vid = cv2.VideoCapture(path)
        
                while(vid.isOpened()):
                    img,frame = vid.read()
                    try:
                        frame = imutils.resize(frame,width=320)
                    except:
                        return
                    a = pickle.dumps(frame)
                    time.sleep(0.05)
                    message = struct.pack("Q",len(a))+a
                    try:
                        client_socket.sendall(message)
                    except:
                        return
    callback("$start_udp_and_play_video")

build_server(handler, 10003, main_menu)