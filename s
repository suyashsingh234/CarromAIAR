s = socket.socket()
print ("socket initilized")

s.bind(('192.168.1.45',9999))

s.listen(2)
print("waiting for the clients")
i = 0
c, addr = s.accept()
while i < 10 :
    
    print("connected with ",addr)
    c.send(bytes('welcome to the network','utf-8'))
    i = i +1
    time.sleep(1)
c.close()


self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((local_ip,port))
        self.s.listen()
        self.clients = []