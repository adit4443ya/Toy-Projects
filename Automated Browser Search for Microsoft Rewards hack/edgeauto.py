import os
import pyautogui as p
import random
import string
import time as t
import keyboard

# Initialize a flag for stopping the program
change_loop = False
s = '#'
stop_program = False
# Function to handle user input


def check_input(e):
    global stop_program
    global change_loop
    if e.name == '+':  # Check if the 's' key is pressed
        change_loop = True
    if e.name == '-':  # Check if the 's' key is pressed
        stop_program = True


# Register the 's' key press event
keyboard.on_press(check_input)


X, Y = p.size()
# edge chalu
os.startfile('https://www.example.com')

# khulne de
t.sleep(2)

# ye randomly string generate karega chanchediyo mat


def randomString(size):
    ch = string.ascii_letters
   # print(len(ch))
    ch = ch+string.digits
    # print(ch)
    randomString = ''
    for i in range(size):
        randomString += random.choice(ch)

    return randomString


r = randomString(35)
# ye actual chiz hogi ek acc me


def dothing():
    global change_loop
    p.typewrite('#')
    t.sleep(0.2)
    p.moveTo(285, 155)
    t.sleep(0.5)
    global s
    s = '#'
    for i in range(34):

        if change_loop:
            change_loop = False
            break
        p.press('enter')
        t.sleep(1)
        p.hotkey('ctrl', 'e')
        s = s+r[i]
        t.sleep(0.1)
        p.typewrite(s)
        t.sleep(4.75)


# yee acc ko badlega
def doing(acc):
    global stop_program
    p.moveTo(360, 60)
    p.click()
    dothing()

    for i in range(acc-1):
     # to that acc option
        if stop_program:
            break
        p.moveTo(X-175, 55)
        t.sleep(0.5)
        p.click()
        t.sleep(0.5)
        # to acc
        p.moveTo(X-180, 425+i*45-90)
        t.sleep(1)
        p.click()
        dothing()
        t.sleep(1)
        p.hotkey('ctrl', 'w')


p.hotkey('ctrl', 't')
# isme jo arguments hai wo number of acc hoga jo tere edge  me hoga
doing(16)
# dothing()
