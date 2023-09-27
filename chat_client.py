
import json
import threading

import websocket


def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        while True:
            message = input("Enter message: ")
            ws.send(json.dumps({'message': message}))
    thread = threading.Thread(target=run)
    thread.start()

if __name__ == "__main__":
    token = input("Enter token: ")
    room_name = input("Enter room name: ")
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(f"ws://localhost:8000/ws/api/chat/{room_name}/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              cookie = f'Token={token}')  # Send token in cookies
    ws.on_open = on_open
    ws.run_forever()
#