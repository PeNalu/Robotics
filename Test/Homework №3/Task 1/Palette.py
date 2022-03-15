import cv2
import math
import numpy as np

img = np.ones((510, 510, 3), np.uint8)
imgHSV = None
mousePos = (0, 0)
value: int = 32


def printPalette():
    global img, imgHSV
    for x in range(510):
        for y in range(510):
            ox = x - 255
            oy = y - 255

            h = math.atan2(ox, oy)
            if h < 0:
                h = 2 * math.pi + h
            h *= 180 / (2 * math.pi)

            s = distance((0, 0), (ox, oy))

            v = value
            if s > 255:
                v = 0

            img[x, y] = (h, s, v)

    imgHSV = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    cv2.imshow("Palette", imgHSV)
    cv2.waitKey(1)

def onValueChange(args):
    global value, img
    value = args
    printPalette()
    printColorCube(imgHSV[mousePos])


def distance(a, b):
    return int(math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])))

def printColorCube(color):
    colorImg = np.ones((200, 200, 3), np.uint8)
    for x in range(200):
        for y in range(200):
            colorImg[x, y] = color

    YCrCbImg = cv2.cvtColor(colorImg, cv2.COLOR_BGR2YCrCb)
    RGBImg = cv2.cvtColor(colorImg, cv2.COLOR_BGR2RGB)
    LABImg = cv2.cvtColor(colorImg, cv2.COLOR_BGR2LAB)
    cv2.imshow("YCrCb", YCrCbImg)
    cv2.imshow("RGB", RGBImg)
    cv2.imshow("LAB", LABImg)


def onMouse(event, x, y, flags, param):
    global mousePos, imgHSV
    if event == cv2.EVENT_LBUTTONDOWN:
        mousePos = (x, y)
        color = imgHSV[mousePos]
        printColorCube(color)


cv2.namedWindow("Palette")
cv2.setMouseCallback("Palette", onMouse)
cv2.createTrackbar("Value", "Palette", value, 255, onValueChange)

printPalette()

while True:
    key = cv2.waitKey(2) & 0xFF

    if key == ord('q'):
        break

cv2.destroyAllWindows()
