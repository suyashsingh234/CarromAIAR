#this file is for network utilities for multiplayer over the network 
import socket
import time
from threading import Thread
import json


def send_move(data,player,clients):
    for client in clients :
        if (client != clients[player]):
            client.send(data)

def recieve_move (player,clients):
    try : 
        move_data = clients[player].recv(1024)
        send_move(move_data,player,clients)
    except :
        print(f"player {player+1} left")
        players=json.dumps([player,"end"])
        if player == 0:
            clients[1].send(players.encode(ascii))
        elif player == 1:
            clients[0].send(players.encode(ascii))
        clients = []

def  accept_connection():
    player = 0
    clients=[]
    for i in range(2):
        print("waiting to connect")
        client,address = server.accept()
        print(f"connected with {str(address)}")
        if player == 0:
            game_sequence = ["human","network"]
            client.send(game_sequence[0].encode('ascii'))
            client.send(game_sequence[1].encode('ascii'))
            clients.append(client)
            player = player +1
        elif player == 1 :
            client.send("network".encode('ascii'))
            client.send("human".encode('ascii'))
            clients[0].send('1'.encode('ascii'))
            clients.append(client)
    while True:
        for i in range(0,len(clients)):
            print("waiting to recieve from ")
            print(i)
            recieve_move(i,clients)
        if (len(clients) != 2):
            break

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(local_ip)
port = 9999
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((local_ip,port))
server.listen()
clients=[]
game_sequence=["network","network"]
player=0
accept_connection()
server.close()
