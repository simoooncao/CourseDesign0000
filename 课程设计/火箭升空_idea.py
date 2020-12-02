'''
原来看的那个找不到了，这个是随手写的，
就是一个在控制台上不断上升的字符化火箭。
'''

import os
from sys import stdout
import time

rocket = '''
 /|\\
/ | \\
  |
  |
 / \\'''

i = 9
while 1:
    i -= 1
    if i <= 0:
        i = 9
    os.system('cls')
    print('\n' * i)
    print(rocket)
    stdout.flush()
    time.sleep(0.2)