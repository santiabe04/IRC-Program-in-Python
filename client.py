'''Client Code'''
import socket
import os
import threading
import crypto as crypto #Change

username = input("Enter your username: ")
user = input('User to ban: ')

host = '127.0.0.1'
port = 55555
cryptokey = crypto.generate_key() #Change

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive_messages():
    '''Is to handle the received messages'''
    while True:
        try:
            message = client.recv(2048)
            message = message.decode("utf-8")

            if message == "@username":
                client.send(username.encode("utf-8"))
            #Change
            elif message == "@key":
                client.send(cryptokey)
            elif message == "@user":
                client.send(user.encode("utf-8"))
            else:
                message = crypto.decrypt((message),cryptokey)
                print(message)
        except:
            print("An error Ocurred")
            client.close
            break

def write_messages():
    '''Is to write in console'''
    while True:
        message = f"{username}: {input('')}"
        #Change
        client.send(crypto.encrypt((message.encode("utf-8")),cryptokey))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()