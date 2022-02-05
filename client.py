from libtcp import build_client
import os

def on_message(message):
    # In ja momkene bekhaym if bezanim age folan chiz bood udp va cv2 va ina ro
    # roshan konim
    print(message, flush=True, end="")

def on_exit():
    os._exit(0)

send_message = build_client(on_message, on_exit, 10001)

while True:
    message = input()
    send_message(message)
