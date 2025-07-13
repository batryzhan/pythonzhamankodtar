import pyautogui 
import time

a = int(input("how many times?: ")

b = input("message: ")

time.sleep(3)

for i in range(a):
    pyautogui.write(b)
    pyautogui.press('enter')

print("done")
