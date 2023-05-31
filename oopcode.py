import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports
import pygame_gui
import cv2
import mediapipe as mp
import pydirectinput
from pynput.keyboard import Key, Controller
import time
from threading import Thread

class game():
    def __init__(self):
        self.__FPS = 32
        self.__chieungangmanhinh = 289
        self.__chieucaomanhinh = 511
        self.__manhinh = pygame.display.set_mode((self.__chieungangmanhinh, self.__chieucaomanhinh))
        self.__GROUNDY = self.__chieucaomanhinh * 0.8
        self.__GAME_SPRITES = {}
        self.__GAME_SOUNDS = {}
        self.__PLAYER = 'image/bird.png'
        self.__BACKGROUND = 'image/background.png'
        self.__PIPE = 'image/pipe.png'
        self.__username = ''
        
        pygame.init() # Initialize all pygame's modules
        
        self.FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption('FlappyBirdPLayWithComputerVision')
        self.__GAME_SPRITES['numbers'] = ( 
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

        self.__GAME_SPRITES['message'] = pygame.image.load('image/message.png').convert_alpha()
        self.__GAME_SPRITES['base'] = pygame.image.load('image/base.png').convert_alpha()
        self.__GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(self.__PIPE).convert_alpha(), 180), 
        pygame.image.load(self.__PIPE).convert_alpha()
        )
        # Game sounds
        pygame.mixer.init()
        self.__GAME_SOUNDS['die'] = pygame.mixer.Sound('audio/die.wav')
        self.__GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.wav')
        self.__GAME_SOUNDS['point'] = pygame.mixer.Sound('audio/point.wav')
        self.__GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
        self.__GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio/wing.wav')

        self.__GAME_SPRITES['background'] = pygame.image.load(self.__BACKGROUND).convert()
        self.__GAME_SPRITES['player'] = pygame.image.load(self.__PLAYER).convert_alpha()
    

    def welcomeScreen(self):
        """
        Shows welcome images on the screen
        """
        manager = pygame_gui.UIManager((289, 511))

        text_input = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((50, 150), (200, 50)), manager=manager,
                                               object_id='#main_text_entry')
        playerx = int(self.__chieungangmanhinh/5)
        playery = int((self.__chieucaomanhinh - self.__GAME_SPRITES['player'].get_height())/2)
        messagex = int((self.__chieungangmanhinh - self.__GAME_SPRITES['message'].get_width())/2)
        messagey = int(self.__chieucaomanhinh*0.13)
        basex = 0
        while True:
            for event in pygame.event.get():
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                # If the user presses space or up key, start the game for them
                elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                    
                    return
                else:
                    self.__manhinh.blit(self.__GAME_SPRITES['background'], (0, 0))    
                    self.__manhinh.blit(self.__GAME_SPRITES['player'], (playerx, playery))    
                    self.__manhinh.blit(self.__GAME_SPRITES['message'], (messagex,messagey ))    
                    self.__manhinh.blit(self.__GAME_SPRITES['base'], (basex, self.__GROUNDY))  
                    pygame.display.update()
                    self.FPSCLOCK.tick(self.__FPS)
                    
    def get_user_name(self):
        WIDTH, HEIGHT = 289, 511
        SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('FlappyBirdPLayWithComputerVision')
        manager = pygame_gui.UIManager((289, 511))

        text_input = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((50, 150), (200, 50)), manager=manager,
                                               object_id='#main_text_entry')
        playerx = int(self.__chieungangmanhinh/5)
        playery = int((self.__chieucaomanhinh - self.__GAME_SPRITES['player'].get_height())/2)
        messagex = int((self.__chieungangmanhinh - self.__GAME_SPRITES['message'].get_width())/2)
        messagey = int(self.__chieucaomanhinh*0.13)
        basex = 0
        self.__manhinh.blit(self.__GAME_SPRITES['background'], (0, 0))    
        self.__manhinh.blit(self.__GAME_SPRITES['player'], (playerx, playery))    
        self.__manhinh.blit(self.__GAME_SPRITES['message'], (messagex,messagey ))    
        self.__manhinh.blit(self.__GAME_SPRITES['base'], (basex, self.__GROUNDY))  

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

    def mainGame(self):
        score = 0
        playerx = int(self.__chieungangmanhinh/5)
        playery = int(self.__chieungangmanhinh/2)
        basex = 0

        # reate 2 pipes for blitting on the screen
        newPipe1 = self.getRandomPipe()
        newPipe2 = self.getRandomPipe()

        # my List of upper pipes
        upperPipes = [
            {'x': self.__chieungangmanhinh+200, 'y':newPipe1[0]['y']},
            {'x': self.__chieungangmanhinh+200+(self.__chieungangmanhinh/2), 'y':newPipe2[0]['y']},
        ]
        # my List of lower pipes
        lowerPipes = [
            {'x': self.__chieungangmanhinh+200, 'y':newPipe1[1]['y']},
            {'x': self.__chieungangmanhinh+200+(self.__chieungangmanhinh/2), 'y':newPipe2[1]['y']},
        ]

        pipeVelX = -4

        playerVelY = -9
        playerMaxVelY = 10
        playerMinVelY = -8
        playerAccY = 1

        playerFlapAccv = -8 # velocity while flapping
        playerFlapped = False # It is true only when the bird is flapping


        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery > 0:
                        playerVelY = playerFlapAccv
                        playerFlapped = True
                        self.__GAME_SOUNDS['wing'].play()


            crashTest = self.isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
            if crashTest:
                return    

            #check for score
            playerMidPos = playerx + self.__GAME_SPRITES['player'].get_width()/2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + self.__GAME_SPRITES['pipe'][0].get_width()/2
                if pipeMidPos<= playerMidPos < pipeMidPos +4:
                    score +=1
                    print(f"Player {self.__username}: score is {score}") 
                    self.__GAME_SOUNDS['point'].play()


            if playerVelY <playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False            
            playerHeight = self.__GAME_SPRITES['player'].get_height()
            playery = playery + min(playerVelY, self.__GROUNDY - playery - playerHeight)

            # move pipes to the left
            for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            # Add a new pipe when the first is about to cross the leftmost part of the screen
            if 0<upperPipes[0]['x']<5:
                newpipe = self.getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            # if the pipe is out of the screen, remove it
            if upperPipes[0]['x'] < -self.__GAME_SPRITES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)
            
            # Lets blit our sprites now
            self.__manhinh.blit(self.__GAME_SPRITES['background'], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                self.__manhinh.blit(self.__GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                self.__manhinh.blit(self.__GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

            self.__manhinh.blit(self.__GAME_SPRITES['base'], (basex, self.__GROUNDY))
            self.__manhinh.blit(self.__GAME_SPRITES['player'], (playerx, playery))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += self.__GAME_SPRITES['numbers'][digit].get_width()
            Xoffset = (self.__chieungangmanhinh - width)/2

            for digit in myDigits:
                self.__manhinh.blit(self.__GAME_SPRITES['numbers'][digit], (Xoffset, self.__chieucaomanhinh*0.12))
                Xoffset += self.__GAME_SPRITES['numbers'][digit].get_width()
            pygame.display.update()
            self.FPSCLOCK.tick(self.__FPS)

    def isCollide(self, playerx, playery, upperPipes, lowerPipes):
        if playery> self.__GROUNDY - 25  or playery<0:
            self.__GAME_SOUNDS['hit'].play()
            return True
        
        for pipe in upperPipes:
            pipeHeight = self.__GAME_SPRITES['pipe'][0].get_height()
            if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < self.__GAME_SPRITES['pipe'][0].get_width()):
                self.__GAME_SOUNDS['hit'].play()
                return True

        for pipe in lowerPipes:
            if (playery + self.__GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < self.__GAME_SPRITES['pipe'][0].get_width():
                self.__GAME_SOUNDS['hit'].play()
                return True

        return False

    def getRandomPipe(self):
        """
        Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
        """
        pipeHeight = self.__GAME_SPRITES['pipe'][0].get_height()
        offset = self.__chieucaomanhinh/3
        y2 = offset + random.randrange(0, int(self.__chieucaomanhinh - self.__GAME_SPRITES['base'].get_height()  - 1.2 *offset))
        pipeX = self.__chieungangmanhinh + 10
        y1 = pipeHeight - y2 + offset
        pipe = [
            {'x': pipeX, 'y': -y1}, #upper Pipe
            {'x': pipeX, 'y': y2} #lower Pipe
        ]
        return pipe

    def run(self):
        while True:
            self.welcomeScreen()
            self.get_user_name() # Shows welcome screen to the user until he presses a button
            self.mainGame() # This is the main game function 
def cv():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    kb = Controller()
    # Ảnh tĩnh
    IMAGE_FILES = []
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:
        for idx, file in enumerate(IMAGE_FILES):
            # Read an image, flip it around y-axis for correct handedness output (see
            # above).
            image = cv2.flip(cv2.imread(file), 1)
            # Convert the BGR image to RGB before processing.
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Điểm.
            print('Handedness:', results.multi_handedness)
            if not results.multi_hand_landmarks:
                continue
            image_height, image_width, _ = image.shape
            annotated_image = image.copy()
            for hand_landmarks in results.multi_hand_landmarks:
                print('hand_landmarks:', hand_landmarks)
                print(
                    f'Index finger tip coordinates: (',
                    f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
                    f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
                )
                mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
            cv2.imwrite(
                '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
            #Vẽ điểm.
            if not results.multi_hand_world_landmarks:
                continue
            for hand_world_landmarks in results.multi_hand_world_landmarks:
                mp_drawing.plot_landmarks(
                hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)

    # webcam:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # chạy vd
                continue

            #
            #
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            #
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Hiển thị tọa độ điểm landmark thứ 9
                    print(hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y)
                    # Khi có tọa độ thì di chuyển đến hoành độ tương ứng màn hình 1920 x1080
                    pydirectinput.moveTo(int((1 - hand_landmarks.landmark[9].x) * 1920), int(hand_landmarks.landmark[9].y * 1080))
                    if hand_landmarks.landmark[4].y > hand_landmarks.landmark[1].y:

                        # and hand_landmarks.landmark[12].y >  hand_landmarks.landmark[11].y and hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y:
                        # pydirectinput.mouseDown()
                        kb.press(Key.space)
                        kb.release(Key.space)
                    elif hand_landmarks.landmark[12].y > hand_landmarks.landmark[11].y and hand_landmarks.landmark[8].y > \
                            hand_landmarks.landmark[7].y:
                        # pydirectinput.mouseUp()
                        kb.press(Key.space)
                        kb.press(Key.space)
                    else:
                        kb.release(Key.space)
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
            # Flip
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
if __name__ == "__main__":        
    game = game()
    play = game.run()
    # Thread(target = game).start()
    # Thread(target = cv).start()
    # game()
    # cv()