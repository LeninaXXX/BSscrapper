import os
import time

cnt = 1
while True:
    try:
        os.system('python main.py -j clarin')
        os.system('python main.py -j infobae')
        os.system('python main.py -j lanacion')
        os.system('python main.py -j radiomitre')
        os.system('python main.py -j la100')		
        print("Esperando...", cnt)
        time.sleep(3600)
        cnt += 1
    except KeyboardInterrupt:
        exit()