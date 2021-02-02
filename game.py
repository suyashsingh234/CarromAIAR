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

display=pygame.display.Info()
width=display.current_w
height=display.current_h

class Board:
    def __init__(self,screen):
        pygame.draw.rect(screen,yellow,[200,50,width-400,50])
        pygame.draw.rect(screen,yellow,[200,height-100,width-400,50])
        pygame.draw.circle(screen,black,(25,25),100)
        pygame.draw.circle(screen,black,(25,height-25),100)
        pygame.draw.circle(screen,black,(width-25,height-25),100)
        pygame.draw.circle(screen,black,(width-25,25),100)
        
def main():
    screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen.fill(blue)
    pygame.display.set_caption("Carrom")
    
    
    b=Board(screen)
    
    running=True
    while running:
        events=pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    running=False
        pygame.display.update()
    pygame.quit()
    sys.exit()

main()