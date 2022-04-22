import cv2
import numpy as np

img = cv2.imread("../../Resources/Paper.jpg")
skin = cv2.imread("../../Resources/GreenMonster.jpg")
skin = cv2.resize(skin, (img.shape[1], img.shape[0]))

value = 0
treshValue = 0

def ChangeSkin(value):
    global skin
    if value == 0:
        return cv2.resize(cv2.imread("../../Resources/abstraction1.jpg"), (img.shape[1], img.shape[0]))
    if value == 1:
        return cv2.resize(cv2.imread("../../Resources/abstraction2.jpg"), (img.shape[1], img.shape[0]))
    if value == 2:
        return cv2.resize(cv2.imread("../../Resources/abstraction3.jpg"), (img.shape[1], img.shape[0]))
    if value == 3:
        return cv2.resize(cv2.imread("../../Resources/abstraction4.jpg"), (img.shape[1], img.shape[0]))
    if value == 4:
        return cv2.resize(cv2.imread("../../Resources/abstraction5.jpg"), (img.shape[1], img.shape[0]))
    else:
        return cv2.resize(cv2.imread("../../Resources/abstraction1.jpg"), (img.shape[1], img.shape[0]))


def onChange(arg):
    global value
    value = arg


def onTreshChange(arg):
    global treshValue
    treshValue = arg


cv2.namedWindow("Image")
cv2.createTrackbar("Treshold", "Image", treshValue, 255, onTreshChange)
cv2.createTrackbar("Value", "Image", value, 5, onChange)

while True:
    print(treshValue)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgGray, treshValue, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros_like(img)
    cv2.drawContours(mask, contours, -1, (255, 255, 255), -1)

    copyImg = img.copy()
    newSkin = ChangeSkin(value)
    copyImg[mask == 255] = newSkin[mask == 255]

    cv2.imshow("Image", copyImg)
    cv2.waitKey(1)
