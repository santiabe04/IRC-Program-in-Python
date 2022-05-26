'''Server Code'''
import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")

clients = []
usernames = []

def ban_client(user):
    '''Is to ban a client from server when an operator executes it'''
    try:
        index = usernames.index(user)
        client = clients[index]
        print(f"{user} disconnected")
        broadcast(f"ChatBot: {user} disconnected".encode('utf-8'), client)
        clients.remove(client)
        usernames.remove(user)
        client.close()
        return True
    except:
        print("Client not found")
        return False

def broadcast(message, _client):
    '''Is to send a message to the clients'''
    for client in clients:
        if client != _client:
            client.send(message)

def handle_messages(client):
    '''Is to handle the received messages'''
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message == "@ban":
                client.send("@user".encode("utf-8"))
                user = client.recv(2048).decode('utf-8')
                result = ban_client(user)
                if(result):
                    client.send("Ban applied".encode("utf-8"))
                else:
                    client.send("Error during ban application".encode("utf-8"))
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            print(f"{username} disconnected")
            broadcast(f"ChatBot: {username} disconnected".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

def receive_connections():
    '''Is to handle a new connection'''
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(2048).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")

        message = f"ChatBot: {username} joined the chat!".encode("utf-8")
        broadcast(message, client)
        client.send("Connected to server".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()