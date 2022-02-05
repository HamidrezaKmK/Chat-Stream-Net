import socket, threading, random

def build_client(on_message, on_exit, port):

    host = "127.0.0.1"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    def write(message):
        client.send(message.encode('ascii'))

    def read():
        while True:
            try:
                message = client.recv(1024).decode('ascii')
                if message == "$special_exit":
                    on_exit()
                    client.close()
                else:
                    on_message(message)
            except Exception as e:
                print(f"Error in handling {e}")
                client.close()
                break

    threadr = threading.Thread(target=read)
    threadr.start()
    return write

def build_server(message_handler, port, init_message):

    host = "127.0.0.1"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    clients = []

    def send_command(i: int, message: str):
        try:
            clients[i].send((message).encode("ascii"))
            if message == "$special_exit":
                clients[i].close()
        except:
            print(f"send command to {i} failed")

    def broadcast(s: str):
        for i in range(len(clients)):
            send_command(i, s)

    def handle(client: socket.socket, i: int):
        while True:
            try:
                message = client.recv(1024).decode('ascii')
            except Exception as e:
                print(f"Error in handling {e}")
                client.close()
                break
            message_handler(message, i, lambda text: send_command(i, text))
            

    while True:
        client, address = server.accept()
        i = len(clients)
        print(f"connected with {address}")
        clients.append(client)
        thread = threading.Thread(target=handle, args=(client, i))
        thread.start()
        send_command(i, init_message)
