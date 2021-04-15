from carrom import Carrom
import random

class AI:
    def __init__(self):
        self.movement=[] #velocity, angle
        self.n=10
        for i in range(self.n):
            vel=random.randint(10,50)
            ang=random.randint(10,100)
            self.movement.append([vel,ang])

    def play(self,carrom):
        index=random.randint(0,9)
        prob=random.randint(0,100)
        if prob<50:
            vel=random.randint(10,50)
            ang=random.randint(10,100)
            carrom.striker.velocity.from_polar((vel,ang))
            if carrom.isPocket:
                self.movement[index]=[vel,ang]
        else:
            carrom.striker.velocity.from_polar((self.movement[index][0],self.movement[index][1]))



