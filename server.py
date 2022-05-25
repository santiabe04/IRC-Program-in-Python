'''Server Code'''
import socket
from _thread import *
import sys

server = "192.168.100.68"
port = 55555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen()

print("Waiting for a connection, Server Started")

def threaded_client(conn, player):
    conn.send(str.encode("Connected"))
    reply = ""
    nameincoming = False
    playername = ""
    messincoming = False
    connected = True
    while connected:
        try:
            data = conn.recv(2048).decode()

            if not data:
                print("Disconnected")
                break
            elif data == "Closing Connection":
                print(str(addr[0]) + " Closed Connection")
                connected = False
            elif nameincoming == True:
                reply = "Name Received"
                print(str(player), " Player Name: ", data)
                playname = data
                nameincoming = False
            elif messincoming == True:
                reply = "Received"
                print("Message Received: ", data)
                conn.sendall(str.encode((str(playername) + " sended " + str(data))))
                messincoming = False
            elif data == "##":
                print("Name in Coming")
                conn.send(str.encode("Waiting for Message..."))
                nameincoming = True
            elif data == "//":
                print("Mess in Coming")
                messincoming = True
            else:
                reply = "Received"
                print("Data Received: ", data)

        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1