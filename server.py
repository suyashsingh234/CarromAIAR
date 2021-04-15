#this file is for network utilities for multiplayer over the network 
import socket
import time
import guigame
from threading import Thread
import guigame

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(local_ip)
port = 9999
class server_runner (Thread):
    def __init__ (self,client,player):
        Thread.__init__(self)
        self.clients = client
        self.player = player
    def send_move(self,data):
        for client in self.clients :
            if (client != self.clients[self.player]):
                client.send(data)

    def recieve_move (self,player):
        while True :
            try : 
                move_data = self.clients[self.player].recv(1024)
                self.send_move(move_data)
            except :
                print(f"player {self.player} left")


        