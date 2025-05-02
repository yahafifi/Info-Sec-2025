import os

for i in range(1,10):
	os.system('ping -c 1 192.168.1.'+str(i))
    