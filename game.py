import random
import sys 
import pygame
from pygame.locals import * 
import pygame_gui
import cv2
import mediapipe as mp
import pydirectinput
from pynput.keyboard import Key, Controller
import time
from threading import Thread
import json

class game():
    ''' Lop xu li game'''
    def __init__(self):
        ''' ham khoi tao cac thanh phan chinh cua game'''
        self.__FPS = 32
        self.__chieungangmanhinh = 289
        self.__chieucaomanhinh = 511
        self.__manhinh = pygame.display.set_mode((self.__chieungangmanhinh, self.__chieucaomanhinh))
        self.__matdat = self.__chieucaomanhinh * 0.8
        self.__hinhanhgame = {}
        self.__amnhacgame = {}
        self.__bird = 'image/bird.png'
        self.__background = 'image/background.png'
        self.__ongnuoc = 'image/pipe.png'
        self.__username = ''
        self.__playerdata = []
        
        pygame.init() # tao cac modules cua pygame
        
        self.FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption('FlappyBirdPLayWithComputerVision')
        self.__hinhanhgame['numbers'] = ( 
            pygame.image.load('image/0.png').convert_alpha(),
            pygame.image.load('image/1.png').convert_alpha(),
            pygame.image.load('image/2.png').convert_alpha(),
            pygame.image.load('image/3.png').convert_alpha(),
            pygame.image.load('image/4.png').convert_alpha(),
            pygame.image.load('image/5.png').convert_alpha(),
            pygame.image.load('image/6.png').convert_alpha(),
            pygame.image.load('image/7.png').convert_alpha(),
            pygame.image.load('image/8.png').convert_alpha(),
            pygame.image.load('image/9.png').convert_alpha(),
        )

        self.__hinhanhgame['message'] = pygame.image.load('image/message.png').convert_alpha()
        self.__hinhanhgame['base'] = pygame.image.load('image/base.png').convert_alpha()
        self.__hinhanhgame['pipe'] = (pygame.transform.rotate(pygame.image.load(self.__ongnuoc).convert_alpha(), 180), 
        pygame.image.load(self.__ongnuoc).convert_alpha()
        )
        # Game sounds
        pygame.mixer.init()
        self.__amnhacgame['die'] = pygame.mixer.Sound('audio/die.wav')
        self.__amnhacgame['hit'] = pygame.mixer.Sound('audio/hit.wav')
        self.__amnhacgame['point'] = pygame.mixer.Sound('audio/point.wav')
        self.__amnhacgame['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
        self.__amnhacgame['wing'] = pygame.mixer.Sound('audio/wing.wav')

        self.__hinhanhgame['background'] = pygame.image.load(self.__background).convert()
        self.__hinhanhgame['player'] = pygame.image.load(self.__bird).convert_alpha()
    

    def manhinhchaomung(self):
        """
        Ham khoi tao man hinh hien thi ban dau
        """
        manager = pygame_gui.UIManager((289, 511))

        text_input = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((50, 150), (200, 50)), manager=manager,
                                               object_id='#main_text_entry')
        playerx = int(self.__chieungangmanhinh/5)
        playery = int((self.__chieucaomanhinh - self.__hinhanhgame['player'].get_height())/2)
        messagex = int((self.__chieungangmanhinh - self.__hinhanhgame['message'].get_width())/2)
        messagey = int(self.__chieucaomanhinh*0.13)
        basex = 0
        while True:
            for event in pygame.event.get():
                # thoat tro choi neu nguoi choi nhan vao nut x
                if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                
                # choi game neu nguoi dung nhan space
                elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                    
                    return
                else:
                    self.__manhinh.blit(self.__hinhanhgame['background'], (0, 0))    
                    self.__manhinh.blit(self.__hinhanhgame['player'], (playerx, playery))    
                    self.__manhinh.blit(self.__hinhanhgame['message'], (messagex,messagey ))    
                    self.__manhinh.blit(self.__hinhanhgame['base'], (basex, self.__matdat))  
                    pygame.display.update()
                    self.FPSCLOCK.tick(self.__FPS)
                    
    def laytennguoichoi(self):
        '''tao man hinh co o text box cho nguoi choi nhap ten dont thoi set thuoc tinh username'''
        WIDTH, HEIGHT = 289, 511
        SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('FlappyBirdPLayWithComputerVision')
        manager = pygame_gui.UIManager((289, 511))

        text_input = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((50, 150), (200, 50)), manager=manager,
                                               object_id='#main_text_entry')
        playerx = int(self.__chieungangmanhinh/5)
        playery = int((self.__chieucaomanhinh - self.__hinhanhgame['player'].get_height())/2)
        messagex = int((self.__chieungangmanhinh - self.__hinhanhgame['message'].get_width())/2)
        messagey = int(self.__chieucaomanhinh*0.13)
        basex = 0
        self.__manhinh.blit(self.__hinhanhgame['background'], (0, 0))    
        self.__manhinh.blit(self.__hinhanhgame['player'], (playerx, playery))    
        self.__manhinh.blit(self.__hinhanhgame['message'], (messagex,messagey ))    
        self.__manhinh.blit(self.__hinhanhgame['base'], (basex, self.__matdat))  

        while True:
            UI_REFRESH_RATE = 32
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                    self.__username = event.text
                    print(self.__username)
                    # self.mainGame()
                    return
                
                manager.process_events(event)
            
            manager.update(UI_REFRESH_RATE)

            # SCREEN.fill("black")

            manager.draw_ui(SCREEN)

            pygame.display.update()
    def luuketquachoi(self, score):
        '''ham luu thong tin nguoi choi'''
        dicttemp = {self.__username:score}
        self.__playerdata.append(dicttemp)
        with open('playerdata.json', 'w') as f:
            json.dump(self.__playerdata, f)


    def mainGame(self):
        '''khoi tao man hinh khi choi game'''
        score = 0
        birdx = int(self.__chieungangmanhinh/5)
        birdy = int(self.__chieungangmanhinh/2)
        basex = 0

        # tao 2 ong nuoc
        ongnuocmoi1 = self.layongngaunhien()
        ongnuocmoi2 = self.layongngaunhien()

        # tao list cac ong nuoc phia tren man hinh
        upperPipes = [
            {'x': self.__chieungangmanhinh+200, 'y':ongnuocmoi1[0]['y']},
            {'x': self.__chieungangmanhinh+200+(self.__chieungangmanhinh/2), 'y':ongnuocmoi2[0]['y']},
        ]
        # tao list cac ong nuoc phia duoi man hinh
        lowerPipes = [
            {'x': self.__chieungangmanhinh+200, 'y':ongnuocmoi1[1]['y']},
            {'x': self.__chieungangmanhinh+200+(self.__chieungangmanhinh/2), 'y':ongnuocmoi2[1]['y']},
        ]

        pipeVelX = -4

        playerVelY = -9
        playerMaxVelY = 10
        playerMinVelY = -8
        playerAccY = 1

        playerFlapAccv = -8 # thay doi toa do khi nhay
        playerFlapped = False # return true neu chim dang nhay


        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if birdy > 0:
                        playerVelY = playerFlapAccv
                        playerFlapped = True
                        self.__amnhacgame['wing'].play()


            crashTest = self.isCollide(birdx, birdy, upperPipes, lowerPipes) # return true neu con chim cham ong nuoc hoac mat dat
            if crashTest:
                self.luuketquachoi(score)
                return    

            #kiem tra diem so
            playerMidPos = birdx + self.__hinhanhgame['player'].get_width()/2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + self.__hinhanhgame['pipe'][0].get_width()/2
                if pipeMidPos<= playerMidPos < pipeMidPos +4:
                    score +=1
                    print(f"Player {self.__username}: score is {score}") 
                    self.__amnhacgame['point'].play()


            if playerVelY <playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False            
            playerHeight = self.__hinhanhgame['player'].get_height()
            birdy = birdy + min(playerVelY, self.__matdat - birdy - playerHeight)

            # di chuyen ong nuoc qua
            for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            # them ong nuoc neu ong nuoc thu nhat da thoat khoi man hinh
            if 0<upperPipes[0]['x']<5:
                newpipe = self.layongngaunhien()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            # xoa ong nuoc neu ong nuoc da ra khoi man hinh
            if upperPipes[0]['x'] < -self.__hinhanhgame['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)
            
            # xu li con chim
            self.__manhinh.blit(self.__hinhanhgame['background'], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                self.__manhinh.blit(self.__hinhanhgame['pipe'][0], (upperPipe['x'], upperPipe['y']))
                self.__manhinh.blit(self.__hinhanhgame['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

            self.__manhinh.blit(self.__hinhanhgame['base'], (basex, self.__matdat))
            self.__manhinh.blit(self.__hinhanhgame['player'], (birdx, birdy))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += self.__hinhanhgame['numbers'][digit].get_width()
            Xoffset = (self.__chieungangmanhinh - width)/2

            for digit in myDigits:
                self.__manhinh.blit(self.__hinhanhgame['numbers'][digit], (Xoffset, self.__chieucaomanhinh*0.12))
                Xoffset += self.__hinhanhgame['numbers'][digit].get_width()
            pygame.display.update()
            self.FPSCLOCK.tick(self.__FPS)

    def isCollide(self, playerx, playery, upperPipes, lowerPipes):
        ''' ham xu li con chim co va cham khong'''
        if playery> self.__matdat - 25  or playery<0:
            self.__amnhacgame['hit'].play()
            return True
        
        for pipe in upperPipes:
            pipeHeight = self.__hinhanhgame['pipe'][0].get_height()
            if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < self.__hinhanhgame['pipe'][0].get_width()):
                self.__amnhacgame['hit'].play()
                return True

        for pipe in lowerPipes:
            if (playery + self.__hinhanhgame['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < self.__hinhanhgame['pipe'][0].get_width():
                self.__amnhacgame['hit'].play()
                return True

        return False

    def layongngaunhien(self):
        """
        ham xu li tao ong nuoc ngau nhien
        """
        pipeHeight = self.__hinhanhgame['pipe'][0].get_height()
        offset = self.__chieucaomanhinh/3
        y2 = offset + random.randrange(0, int(self.__chieucaomanhinh - self.__hinhanhgame['base'].get_height()  - 1.2 *offset))
        pipeX = self.__chieungangmanhinh + 10
        y1 = pipeHeight - y2 + offset
        pipe = [
            {'x': pipeX, 'y': -y1}, #upper Pipe
            {'x': pipeX, 'y': y2} #lower Pipe
        ]
        return pipe

    def run(self):
        '''ham chay game/ cac thanh phan cua game'''
        while True:
            self.manhinhchaomung() # man hinh chao mung nguoi choi
            self.laytennguoichoi() # man hinh de nguoi choi nhap ten
            self.mainGame() # man hinh choi game chinh 

