import cv2
import math
import numpy as np
import random
import string

img = cv2.imread("../../Resources/Card.jpg")
imgCopy = img.copy()
points = []
images = []

def draw_circle(event, x, y, flags, param):
    if len(points) == 4:
        return

    global mouseX, mouseY
    if  event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), 2, (255, 0, 0), -1)
        mouseX, mouseY = x, y
        points.append((x, y))

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def distance(a, b):
    return math.sqrt((math.pow(a[0] - b[0], 2) + (math.pow(a[1] - b[1], 2))))

def drawcard(point1, point2, point3, pont4):
    width = 200
    height = 300
    pts1 = np.float32([[point1], [point2], [point3], [pont4]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(imgCopy, matrix, (width, height))
    windowName = generate_random_string(5)
    images.append((windowName, imgOutput))

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

while True:
    cv2.imshow('image', img)
    if len(points) == 4:
        drawcard(points[0], points[1], points[2], points[3])
        points.clear()
    for name, image in images:
        cv2.imshow(name, image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

