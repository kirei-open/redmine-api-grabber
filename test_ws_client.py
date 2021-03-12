from websocket import create_connection

ws = create_connection("ws://localhost:8000/ws")
print("sending packet")
ws.send("packet")
print("sent")
print("receiving")
while True:
    result=ws.recv()
    print(result)