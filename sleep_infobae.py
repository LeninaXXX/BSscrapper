# wait_infobae.py
import os
import time

print("Remember first to start the virtual environment!")

while True:
    try:
        print('\t\t+++LAUNCHING!!!')
        print('\t\t' + '=' * len('+++LAUNCHING!!!'))
        print('\t\t' + '=' * len('+++LAUNCHING!!!'))
        os.system('python main.py -j infobae')
        print('\t\t+++WAITING 20 MINUTES!!!')
        print('\t\t' + '=' * len('+++WAITING 20 MINUTES!!!'))
        print('\t\t' + '=' * len('+++WAITING 20 MINUTES!!!'))
        time.sleep(1200)
    except KeyboardInterrupt:
        exit()
