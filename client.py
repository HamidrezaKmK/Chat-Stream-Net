from libtcp import build_client
import os
import clientstream
from queue import Queue
import socket, threading, random

q = Queue()

def establish_UDP_connection(port, ip):
    print("established.")
    print(ip)
    print(port)
    clientstream.get_stream(port, ip)

def on_message(message):
    message_splitted = message.split()
    if message_splitted[0] == '[PORTREQ]':
        port = int(message_splitted[1])
        ip = message_splitted[2]
        q.put((port, ip))
    
    # In ja momkene bekhaym if bezanim age folan chiz bood udp va cv2 va ina ro
    # roshan konim
    print(message, flush=True, end="")

def on_exit():
    os._exit(0)

send_message = build_client(on_message, on_exit, 10001)

def inp():
    while True:
        message = input()
        send_message(message)

tinp = threading.Thread(target=inp)
tinp.start()

while True:
    port, ip = q.get()
    establish_UDP_connection(port, ip)