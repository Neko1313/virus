import keyboard
from time import sleep

def lock_key():
    for i in range(150):
        keyboard.block_key(i)

def unlock_key():
    for i in range(150):
        keyboard.unblock_key(i)

