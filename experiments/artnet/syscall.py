import os
import subprocess
import re
import time

while True:

    output = subprocess.check_output("cat /home/pi/drie", shell=True)
    a = re.sub('\D', '', output.decode('utf-8'))
    print("aantal is nu: {}".format(a))

    a = int(a)

    for i in range (a, 0, -1):
        print (i)
    print("even tukken") 
    time.sleep(10)
#    for step in range (0,48,8):
#        print(f"step is nu {step} en we gaan breathe aanroepen")
