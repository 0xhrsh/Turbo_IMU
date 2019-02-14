import serial
import ctypes
import time
import numpy as np
from PIL import ImageGrab
#import cv2
import time
#import pyautogui

SendInput = ctypes.windll.user32.SendInput


W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

if __name__ == '__main__':
    i=0
    arduino = serial.Serial('COM3', baudrate=9600, timeout=.1)
    while i<20:
        data = arduino.readline()
        time.sleep(0.1)
        i+=1
    while True :
        data = arduino.readline()[:-2]
        print(data)
        data=data.split()
        data[0]=int(data[0])
        data[1]=int(data[1])
        if data[1]>10000:
            PressKey(A)
            time.sleep(0.035)
            ReleaseKey(A)
            time.sleep(0.005)
        if data[1]<-10000:
            PressKey(D)
            time.sleep(0.035)
            ReleaseKey(D)
            time.sleep(0.005)
        if data[0]>10000:
            PressKey(S)
            time.sleep(0.035)
            ReleaseKey(S)
            time.sleep(0.005)
        if data[0]<100:
            PressKey(W)
            time.sleep(0.045)
            ReleaseKey(W)
            time.sleep(0.005)