from carrom import Carrom
from pygame import Rect
import pygame
from start_menu import start_window, create_button
import cv2
from ai import AI
import time
from threading import Thread
import socket
import json
import argparse

class Guigame:
    def __init__(self):
        self.player1=1
        self.player2=2
        self.width=700
        self.max_angle=80
        self.max_speed=40
        self.dt=0.1
        self.decelerate=0.3
        self.e=0.9
        self.num_updates=10
        self.fps=60
        self.ai=AI()
    def parser_args(self):
        parser = argparse.ArgumentParser(description='This program is a gui for carrom game')
        parser.add_argument('-ip', type=str,metavar='', action='store',default='0.0.0.0',help='enter this if you want to play game over the network')

        args = parser.parse_args()
        n = args.ip
        print(n)
        return n
# Add gamestarter to the start with the camera 
    def gamestarter (self):
        self.player1, self.player2 = start_window(self.width,self.fps)
        print(self.player1)
        print(self.player2)
        if(self.player1 == "network"):
            self.connection = socket.socket()
            #self.connectip=input("Enter the ip address of the server to connect to \n")
            self.connectip = self.parser_args()
            self.connection.connect((self.connectip,9999))
            self.player1 = self.connection.recv(1024).decode('ascii')
            self.player2 = self.connection.recv(1024).decode('ascii')
            start = 0
            print(self.player1)
            print(self.player2)
            while (start == 0):
                print("waiting to start game ")
                if (self.player1 == "network" and self.player2 == "human"):
                    start = 1
                else :
                    start = self.connection.recv(1024).decode('ascii')
                print(start)

        """ Printing game constraints """
        print("Parameters are width:", self.width, "dt:", self.dt, "decelerate:", self.decelerate, "e:", self.e, "max_angle:", self.max_angle,
            "max_speed:", self.max_speed, "num_updates:", self.num_updates, "fps:", self.fps, "player1:", self.player1, "player2:", self.player2)
        pygame.init()
        self.win = pygame.display.set_mode((self.width, self.width))
        pygame.display.set_caption("PyCarrom: WHITE(%s) vs BLACK(%s)" % (self.player1, self.player2))
        self.carrom = Carrom(Rect(0, 0, self.width, self.width))
        self.players = [self.player1, self.player2]
        print(self.players)
        self.clock = pygame.time.Clock()
        pygame.display.update()
    # Will be called inside the class 
    def handle_events(self):
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                pygame.quit()
                quit()
    # to be planned to be called from the camera window
    #currently it is called inside the class
    def handle_user_input(self,win_, carrom_):
        get_user_input = True
        striker_speed = 0
        striker_angle = 0
        coins_orientation = 60

        x_limits = carrom_.board.get_striker_x_limits()
        
        while get_user_input:
            self.clock.tick(self.fps)
            for event_ in pygame.event.get():
                if event_.type == pygame.QUIT:
                    pygame.quit()

            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
                print(carrom_.striker.position.x)
                carrom_.striker.position.x -= 4 if not pressed[pygame.K_LSHIFT] else 0.5
            if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
                print(carrom_.striker.position.x)
                carrom_.striker.position.x += 4 if not pressed[pygame.K_LSHIFT] else 0.5

            if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
                print(striker_speed)
                striker_speed -= self.max_speed * 0.05 if not pressed[pygame.K_LSHIFT] else self.max_speed * 0.005
            if pressed[pygame.K_w] or pressed[pygame.K_UP]:
                print(striker_speed)
                striker_speed += self.max_speed * 0.05 if not pressed[pygame.K_LSHIFT] else self.max_speed * 0.005

            if pressed[pygame.K_q]:
                print(striker_angle)
                striker_angle += self.max_angle * 0.05 if not pressed[pygame.K_LSHIFT] else self.max_angle * 0.005
            if pressed[pygame.K_e]:
                print(striker_angle)
                striker_angle -= self.max_angle * 0.05 if not pressed[pygame.K_LSHIFT] else self.max_angle * 0.005
            if pressed[pygame.K_z]:
                pygame.quit()
                quit()
            carrom_.striker.position.x = min(x_limits[1], max(x_limits[0], carrom_.striker.position.x))
            striker_speed = min(self.max_speed, max(striker_speed, 0))
            striker_angle = min(self.max_angle, max(-self.max_angle, striker_angle))
            carrom_.striker.velocity.from_polar(
                (striker_speed, -90-striker_angle if carrom_.player_turn == 0 else 90+striker_angle))

            if pressed[pygame.K_SPACE]:
                get_user_input = False
                if("network" in self.players):
                    move=[striker_speed,-90-striker_angle if carrom_.player_turn == 0 else 90+striker_angle,carrom_.striker.position.x]
                    print(move)
                    y = json.dumps(move)
                    print(type(y))
                    try :
                        self.connection.send(y.encode('ascii'))
                    except :
                        print("the game has ended due to some issue")
                        self.connection.close()
                #send data to the server to be communicated 

            carrom_.draw(win_)
            carrom_.board.show_notification(win_, "WHITE'S TURN" if carrom_.player_turn == 0 else "BLACK'S TURN")
            carrom_.board.draw_striker_arrow_pointer(win_, carrom_.striker, self.max_speed)
            pygame.display.update()
    # run this and check for the game status 
    def check_game_over(self):
        return self.carrom.game_over
    #expose the pygame surface 
    def board_state(self):
        try:
            pygame.image.save(self.win,"tmp.jpg")
            return 0
        except:
            return 1
    # if game not over than keep this running in the while 
    def gamerunner(self):
        self.carrom.striker.position = self.carrom.board.get_striker_position(self.carrom.player_turn)
        if self.players[self.carrom.player_turn] == "ai" :
            """ Just refresh the board """
            self.ai.play(self.carrom)
        elif self.players[self.carrom.player_turn] == "network":
            print("waiting for input from the network")
            data = self.connection.recv(4096).decode('ascii')
            d = json.loads(data)
            if (d[0] == str(self.players.index('network')) and d[1] == "end"):
                self.game_ender()
            else :
                self.carrom.striker.position.x = d[2]
                self.carrom.striker.velocity.from_polar((d[0],d[1]))
        else :
            self.handle_user_input(self.win, self.carrom)
            pygame.time.delay(100)

        i = 0
        while self.carrom.check_moving():
            self.carrom.update(self.dt, self.decelerate, self.e)
            if self.carrom.check_moving():
                i += 1
                if i % self.num_updates == 0:
                    self.clock.tick(self.fps)
                    self.carrom.draw(self.win)
                    self.carrom.board.show_notification(self.win, "SIMULATING..")
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            if ("network" in self.players):
                                self.connection.close()
                            
                            pygame.quit()
                            quit()
        self.carrom.apply_rules()
    #call as the game ends 
    def game_ender(self):
        self.carrom.draw(self.win)
        self.carrom.board.show_notification(self.win, "GAME OVER..")
        font = pygame.font.Font('freesansbold.ttf', self.carrom.board.frame_width)
        winner = self.carrom.get_player(self.carrom.winner)
        print("Game Over, won by", winner, self.players[self.carrom.winner])
        if ("network" in self.players):
            self.connection.close()
        text = font.render("WINNER " + winner, True, (0, 0, 255))
        text_rect = text.get_rect()
        text_rect.center = self.carrom.board.board.center
        self.win.blit(text, text_rect)
        width = self.width
        self.restart_button = create_button(width*3//10, width//10, "RESTART", False)
        self.restart_button_rect = Rect(width*1//10, width*7//10, width*3//10, width//10)
        self.quit_button = create_button(width*3//10, width//10, "QUIT", False)
        self.quit_button_rect = Rect(width*6//10, width*7//10, width*3//10, width//10)
        self.win.blit(self.restart_button, self.restart_button_rect)
        self.win.blit(self.quit_button, self.quit_button_rect)
        pygame.display.update()
    #keep this runnung in the while
    def updater(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_f]:
            if ("network" in self.players):
                print("cant fast forward a game over the network")
            else :
                self.fps=1000000
        else:
            self.fps=60
        if pressed[pygame.K_z]:
            self.game_quit

        self.clock.tick(self.fps)
        self.handle_events()
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            # Add restart mechanism 
            #if self.restart_button_rect.collidepoint(*mouse_pos):
            #    break
            if self.quit_button_rect.collidepoint(*mouse_pos):
                pygame.quit()
                quit()
    def game_quit (self):
        if ("network" == self.player1 or self.player2 == "network"):
            self.connection.close()
        pygame.quit()
        quit()

class runner(Thread,Guigame):
    def __init__ (self):
        Thread.__init__(self)
        self.game = Guigame()

    def run(self):
        self.game.gamestarter()
        while True :
            if not self.game.check_game_over():
                self.game.gamerunner()
            self.game.updater()
        self.game.game_ender() 
    def board_state_sender(self):
        return self.game.board_state() 
