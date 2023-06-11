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
def game():
    
    FPS = 32
    chieungangmanhinh = 289
    chieucaomanhinh = 511
    manhinhh = pygame.display.set_mode((chieungangmanhinh, chieucaomanhinh))
    GROUNDY = chieucaomanhinh * 0.8
    hinhanhgame = {}
    amnhacgame = {}
    bird = 'image/bird.png'
    BACKGROUND = 'image/background.png'
    ongnuoc = 'image/pipe.png'
    username = ''
    playerdata = []


    def manhinhchaomung():
        """
        Ham khoi tao man hinh hien thi ban dau
        """
        FPSCLOCK = pygame.time.Clock()
        manager = pygame_gui.UIManager((289, 511))

        text_input = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((50, 150), (200, 50)), manager=manager,
                                                object_id='#main_text_entry')
        playerx = int(chieungangmanhinh/5)
        playery = int((chieucaomanhinh - hinhanhgame['player'].get_height())/2)
        messagex = int((chieungangmanhinh - hinhanhgame['message'].get_width())/2)
        messagey = int(chieucaomanhinh*0.13)
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
                    manhinhh.blit(hinhanhgame['background'], (0, 0))    
                    manhinhh.blit(hinhanhgame['player'], (playerx, playery))    
                    manhinhh.blit(hinhanhgame['message'], (messagex,messagey ))    
                    manhinhh.blit(hinhanhgame['base'], (basex, GROUNDY))  
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                    
    def laytennguoichoi():
        '''tao man hinh co o text box cho nguoi choi nhap ten dont thoi set thuoc tinh username'''
        WIDTH, HEIGHT = 289, 511
        SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('FlappyBirdPLayWithComputerVision')
        manager = pygame_gui.UIManager((289, 511))

        text_input = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((50, 150), (200, 50)), manager=manager,
                                                object_id='#main_text_entry')
        playerx = int(chieungangmanhinh/5)
        playery = int((chieucaomanhinh - hinhanhgame['player'].get_height())/2)
        messagex = int((chieungangmanhinh - hinhanhgame['message'].get_width())/2)
        messagey = int(chieucaomanhinh*0.13)
        basex = 0
        manhinhh.blit(hinhanhgame['background'], (0, 0))    
        manhinhh.blit(hinhanhgame['player'], (playerx, playery))    
        manhinhh.blit(hinhanhgame['message'], (messagex,messagey ))    
        manhinhh.blit(hinhanhgame['base'], (basex, GROUNDY))  

        while True:
            UI_REFRESH_RATE = 32
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                    global username
                    username = event.text
                    print(username)
                    # mainGame()
                    return
                
                manager.process_events(event)
            
            manager.update(UI_REFRESH_RATE)

            # SCREEN.fill("black")

            manager.draw_ui(SCREEN)

            pygame.display.update()
    def luuketquachoi(username, score):
        '''ham luu thong tin nguoi choi'''
        dicttemp = {username:score}
        playerdata.append(dicttemp)
        with open('playerdata.json', 'w') as f:
            json.dump(playerdata, f)


    def mainGame():
        '''khoi tao man hinh khi choi game'''
        score = 0
        playerx = int(chieungangmanhinh/5)
        playery = int(chieungangmanhinh/2)
        basex = 0

        # tao 2 ong nuoc
        newPipe1 = layongngaunhien()
        newPipe2 = layongngaunhien()

        # tao list cac ong nuoc phia tren man hinh
        upperPipes = [
            {'x': chieungangmanhinh+200, 'y':newPipe1[0]['y']},
            {'x': chieungangmanhinh+200+(chieungangmanhinh/2), 'y':newPipe2[0]['y']},
        ]
        # tao list cac ong nuoc phia duoi man hinh
        lowerPipes = [
            {'x': chieungangmanhinh+200, 'y':newPipe1[1]['y']},
            {'x': chieungangmanhinh+200+(chieungangmanhinh/2), 'y':newPipe2[1]['y']},
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
                    if playery > 0:
                        playerVelY = playerFlapAccv
                        playerFlapped = True
                        amnhacgame['wing'].play()


            crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # return true neu con chim cham ong nuoc hoac mat dat
            if crashTest:
                luuketquachoi(username, score)
                return    

            #kiem tra diem so
            playerMidPos = playerx + hinhanhgame['player'].get_width()/2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + hinhanhgame['pipe'][0].get_width()/2
                if pipeMidPos<= playerMidPos < pipeMidPos +4:
                    score +=1
                    print(f"Player {username}: score is {score}") 
                    amnhacgame['point'].play()


            if playerVelY <playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False            
            playerHeight = hinhanhgame['player'].get_height()
            playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

            # di chuyen ong nuoc qua
            for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            # them ong nuoc neu ong nuoc thu nhat da thoat khoi man hinh
            if 0<upperPipes[0]['x']<5:
                newpipe = layongngaunhien()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            # xoa ong nuoc neu ong nuoc da ra khoi man hinh
            if upperPipes[0]['x'] < -hinhanhgame['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)
            
            # xu li con chim
            manhinhh.blit(hinhanhgame['background'], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                manhinhh.blit(hinhanhgame['pipe'][0], (upperPipe['x'], upperPipe['y']))
                manhinhh.blit(hinhanhgame['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

            manhinhh.blit(hinhanhgame['base'], (basex, GROUNDY))
            manhinhh.blit(hinhanhgame['player'], (playerx, playery))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += hinhanhgame['numbers'][digit].get_width()
            Xoffset = (chieungangmanhinh - width)/2

            for digit in myDigits:
                manhinhh.blit(hinhanhgame['numbers'][digit], (Xoffset, chieucaomanhinh*0.12))
                Xoffset += hinhanhgame['numbers'][digit].get_width()
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def isCollide( playerx, playery, upperPipes, lowerPipes):
        ''' ham xu li con chim co va cham khong'''
        if playery> GROUNDY - 25  or playery<0:
            amnhacgame['hit'].play()
            return True
        
        for pipe in upperPipes:
            pipeHeight = hinhanhgame['pipe'][0].get_height()
            if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < hinhanhgame['pipe'][0].get_width()):
                amnhacgame['hit'].play()
                return True

        for pipe in lowerPipes:
            if (playery + hinhanhgame['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < hinhanhgame['pipe'][0].get_width():
                amnhacgame['hit'].play()
                return True

        return False

    def layongngaunhien():
        """
        ham xu li tao ong nuoc ngau nhien
        """
        pipeHeight = hinhanhgame['pipe'][0].get_height()
        offset = chieucaomanhinh/3
        y2 = offset + random.randrange(0, int(chieucaomanhinh - hinhanhgame['base'].get_height()  - 1.2 *offset))
        pipeX = chieungangmanhinh + 10
        y1 = pipeHeight - y2 + offset
        pipe = [
            {'x': pipeX, 'y': -y1}, #upper Pipe
            {'x': pipeX, 'y': y2} #lower Pipe
        ]
        return pipe

    FPS = 32
    chieungangmanhinh = 289
    chieucaomanhinh = 511
    manhinhh = pygame.display.set_mode((chieungangmanhinh, chieucaomanhinh))
    GROUNDY = chieucaomanhinh * 0.8
    hinhanhgame = {}
    amnhacgame = {}
    bird = 'image/bird.png'
    BACKGROUND = 'image/background.png'
    ongnuoc = 'image/pipe.png'
    username = ''
    playerdata = []
    pygame.init() # tao cac modules cua pygame

    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('FlappyBirdPLayWithComputerVision')
    hinhanhgame['numbers'] = ( 
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

    hinhanhgame['message'] = pygame.image.load('image/message.png').convert_alpha()
    hinhanhgame['base'] = pygame.image.load('image/base.png').convert_alpha()
    hinhanhgame['pipe'] = (pygame.transform.rotate(pygame.image.load(ongnuoc).convert_alpha(), 180), 
    pygame.image.load(ongnuoc).convert_alpha()
    )
    # Game sounds
    pygame.mixer.init()
    amnhacgame['die'] = pygame.mixer.Sound('audio/die.wav')
    amnhacgame['hit'] = pygame.mixer.Sound('audio/hit.wav')
    amnhacgame['point'] = pygame.mixer.Sound('audio/point.wav')
    amnhacgame['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    amnhacgame['wing'] = pygame.mixer.Sound('audio/wing.wav')

    hinhanhgame['background'] = pygame.image.load(BACKGROUND).convert()
    hinhanhgame['player'] = pygame.image.load(bird).convert_alpha()
    while True:
            manhinhchaomung() # man hinh chao mung nguoi choi
            laytennguoichoi() # man hinh de nguoi choi nhap ten
            mainGame() # man hinh choi game chinh 
def cv():
    kb = Controller()
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    # Đối với xử lý ảnh tĩnh
    IMAGE_FILES = []
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:
        for idx, file in enumerate(IMAGE_FILES):
            #Xoay ảnh theo trục tọa độ y
            image = cv2.flip(cv2.imread(file), 1)
            #Chuyển đổi kênh màu
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Xử lý điểm ảnh
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

    # Đối với xử lý webcam:
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

            #Chuyển đổi kênh màu cho web cam
            #từ rgb bgr qua rgb
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            #Gọi flag để xử lý màu hình ảnh
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Hiển thị tọa độ điểm landmark thứ 9
                    #print(hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y)
                    # Khi có tọa độ thì di chuyển đến hoành độ tương ứng màn hình 1920 x1080
                    pydirectinput.moveTo(int((1 - hand_landmarks.landmark[9].x) * 1920), int(hand_landmarks.landmark[9].y * 1080))
                    if hand_landmarks.landmark[4].y > hand_landmarks.landmark[1].y:

                        # and hand_landmarks.landmark[12].y >  hand_landmarks.landmark[11].y and hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y:
                        # pydirectinput.mouseDown()
                        kb.press(Key.space)
                        kb.release(Key.space)
                        print('nhan cu chi nhay mot lan')
                    elif hand_landmarks.landmark[12].y > hand_landmarks.landmark[11].y and hand_landmarks.landmark[8].y > \
                            hand_landmarks.landmark[7].y:
                        # pydirectinput.mouseUp()
                        kb.press(Key.space)
                        kb.press(Key.space)
                        print('nhan cu chi nhay 2 lan')
                    elif (hand_landmarks[8].y - hand_landmarks[7].y)  <= (hand_landmarks[4].y - hand_landmarks[3].y):
                        kb.press(Key.space)
                        kb.press(Key.space)
                        kb.press(Key.space)
                        print('nhan cu chi nhay 3 lan khi nhan dien tay ban tim')
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
    Thread(target = cv).start()   
    # Thread(target = game).start()
