import os
import time

cnt = 1
while True:
	try:
		os.system('python main.py -dc -j clarin')
		os.system('python main.py -dc -j infobae')
		os.system('python main.py -dc -j lanacion')
		os.system('python main.py -dc -j radiomitre')
		os.system('python main.py -dc -j la100')
		print("Esperando...", cnt)
		time.sleep(3600)
		cnt += 1
	except KeyboardInterrupt:
		exit()