import socket,cv2, pickle,struct

def get_stream(port, ip, q):
    
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = ip
    port = port
    client_socket.connect((host_ip,port))
    data = b""
    payload_size = struct.calcsize("Q")

    print("Here")
    
    try:
        flag = True
        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024) # 4K
                if not packet:
                    flag = False
                    break
                data += packet
            if (flag == False):
                break
            packed_msg_size = data[:payload_size]
            #print(packed_msg_size)
            data = data[payload_size:]
            
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("RECEIVING VIDEO",frame)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                break
            try:
                if (q.get(False) == "exit"):
                    break
            except:
                pass
        print("here before closing")
        cv2.destroyAllWindows()
        client_socket.close()
    except KeyboardInterrupt:
        client_socket.close()
