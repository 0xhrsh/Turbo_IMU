import serial
import ctypes
import time
import numpy as np
from PIL import ImageGrab
#import cv2
import time
#import pyautogui

SendInput = ctypes.windll.user32.SendInput


def filter(x, yaxis):
    positiveThrehold = 0.3
    negativeThrehold = -0.3

    # if yaxis:
    #     positiveThrehold = -0.1
    #     negativeThrehold = -0.3

    if x > positiveThrehold:
        return 1
    elif x < negativeThrehold:
        return -1
    else:
        return 0


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
                ("time", ctypes.c_ulong),
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
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002,
                        0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

SLEEP_TIME = 0.03


if __name__ == '__main__':
    i = 0
    arduino = serial.Serial('COM8', baudrate=9600, timeout=.1)
    while i < 10:
        data = arduino.readline()
        time.sleep(0.1)
        i += 1
    while True:
        data = arduino.readline()[:-2].decode('utf8')
        try:
            data = data.split(',')
            data[0] = filter(float(data[0]), False)
            data[1] = filter(float(data[1]), True)
            print(data[0], data[1])
        except:
            continue
        if data[1] < 0:
            PressKey(W)
            time.sleep(SLEEP_TIME + 0.01)
            ReleaseKey(W)
            time.sleep(0.001)
        if data[1] > 0:
            PressKey(S)
            time.sleep(SLEEP_TIME)
            ReleaseKey(S)
            time.sleep(0.001)

        if data[0] > 0:
            PressKey(A)
            time.sleep(SLEEP_TIME)
            ReleaseKey(A)
            time.sleep(0.001)
        if data[0] < 0:
            PressKey(D)
            time.sleep(SLEEP_TIME)
            ReleaseKey(D)
            time.sleep(0.001)
