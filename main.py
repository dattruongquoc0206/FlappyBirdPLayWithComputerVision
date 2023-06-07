from game import *
from cv import *
from threading import Thread

if __name__ == "__main__":        
    ''' hàm gọi các đối tượng cử chỉ'''
    #chay game khong co cu chi tay
    game = game()
    cv = cv()
    #chay game khong co cu chi tay
    play1 = game.run()
    #neu muon chay game voi cu chi tay vui long bo che do command dong code duoi day 
    # Thread(target = game.run()).start()
    # Thread(target = cv.run()).start()

    #HOAC CHAY FILE mainno.py nếu thiết bị của bạn không đáp ứng đủ phần cứng xử lý