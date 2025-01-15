from pyautogui import moveTo, press
from time import sleep
from random import randint

for i in range(20):
    press('volumemute')
    x = randint(1, 1000)
    y = randint(1, 1000)
    press('volumeup')
    moveTo(x , y, 5)
    press('capslock')
    sleep(10)
    press('capslock')
   