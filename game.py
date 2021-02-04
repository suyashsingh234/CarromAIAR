# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 11:08:50 2021

@author: Suyash Singh
"""
import pygame, sys
from pygame.locals import *
pygame.init()
    
black=(0,0,0)
blue=(137,207,240)
yellow=(235, 201, 52)
purple=(152, 60, 158)

display=pygame.display.Info()
width=display.current_w
height=display.current_h

screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen.fill(blue)
pygame.display.set_caption("Carrom")

class Board:
    def __init__(self):
        self.upperRow=[200,50,width-400,50]
        self.lowerRow=[200,height-100,width-400,50]
        self.holeRadius=100
        self.holes=[[25,25],[25,height-25],[width-25,height-25],[width-25,25]]
        
        self.midUpper=[ self.upperRow[0]+self.upperRow[2]//2, self.upperRow[1]+self.upperRow[3]//2 ]   # x y 
        self.midLower=[ self.lowerRow[0]+self.lowerRow[2]//2, self.lowerRow[1]+self.lowerRow[3]//2 ]
        
    def draw(self):
        pygame.draw.rect(screen,yellow,self.upperRow)
        pygame.draw.rect(screen,yellow,self.lowerRow)
        pygame.draw.circle(screen,black,self.holes[0],self.holeRadius)
        pygame.draw.circle(screen,black,self.holes[1],self.holeRadius)
        pygame.draw.circle(screen,black,self.holes[2],self.holeRadius)
        pygame.draw.circle(screen,black,self.holes[3],self.holeRadius)
        
class Striker:
    def __init__(self):
        self.x=0
        self.y=0
        self.radius=50
        
    def draw(self,position):
        self.x=position[0]
        self.y=position[1]
        pygame.draw.circle(screen,purple,[self.x,self.y],self.radius)
        
        
def draw_window():
    board=Board()
    board.draw()
    striker=Striker()
    mouseX,mouseY=pygame.mouse.get_pos()
    striker.draw([mouseX,board.midLower[1]])
        
def main():
    lowerPlayer=True
    
    running=True
    while running:
        
        events=pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    running=False
        screen.fill(blue)       
        draw_window()
                    
        pygame.display.update()
        pygame.time.Clock().tick(40)
    pygame.quit()
    sys.exit()

main()