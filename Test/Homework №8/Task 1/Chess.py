import math
from matplotlib import pyplot as plt
import cv2
import numpy as np


def distance(pt1, pt2):
    return int(math.sqrt((pt1[0] - pt2[0]) * (pt1[0] - pt2[0]) + (pt1[1] - pt2[1]) * (pt1[1] - pt2[1])))


cellSize = 2
minX, minY = 350, 350
maxX, maxY = 0, 0
cellCorners = []
points: list[tuple[int, int]] = []

img = cv2.imread("../../Resources/1.jpg")
coinImg = cv2.imread("../../Resources/2.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 0, 0.02, 10)
corners = np.int0(corners)

for i in corners:
    x, y = i.ravel()
    points.append((x, y))
    cv2.circle(img, (x, y), 3, 255, -1)

cannyCoin = cv2.Canny(coinImg, 700, 700)
contours, hierarchy = cv2.findContours(cannyCoin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

index = 0
maxContourLength = 0
maxIndex = 0
for a in contours:
    if maxContourLength < len(a):
        maxContourLength = len(a)
        maxIndex = index
    index += 1

mask = np.zeros_like(coinImg)
cv2.drawContours(mask, contours, maxIndex, (255, 255, 255), -1)

for a in contours[maxIndex]:
    if a[0][0] < minX:
        minX = a[0][0]
    if a[0][0] > maxX:
        maxX = a[0][0]
    if a[0][1] < minY:
        minY = a[0][1]
    if a[0][1] > maxY:
        maxY = a[0][1]

cv2.rectangle(coinImg, (minX, minY), (maxX, maxY), (0, 0, 255), 1)
corners = [(minX, minY), (minX, maxY), (maxX, maxY), (maxX, minY)]

for a in corners:
    minDistance = 350
    index = 0
    for i in range(len(points)):
        if distance(a, points[i]) < minDistance:
            minDistance = distance(a, points[i])
            index = i

    cellCorners.append(index)

cv2.rectangle(coinImg, points[cellCorners[0]], points[cellCorners[2]], (255, 0, 0), 1)

cellWidth = distance(points[cellCorners[1]], points[cellCorners[2]])
cellHeight = distance(points[cellCorners[0]], points[cellCorners[1]])

objectWidth = distance(corners[1], corners[2])
objectHeight = distance(corners[0], corners[1])

realObjectWidth = math.floor((objectWidth * cellSize) / cellWidth * 100)
realObjectHeight = math.floor((objectHeight * cellSize) / cellHeight * 100)

print(f'Ширина - {realObjectWidth} миллиметра \nВысота - {realObjectHeight} миллиметра')

plt.subplot(221), plt.imshow(cannyCoin, cmap='gray')
plt.title('Canny'), plt.xticks([]), plt.yticks([])
plt.subplot(222), plt.imshow(mask, cmap='gray')
plt.title('Canny Mask'), plt.xticks([]), plt.yticks([])
plt.subplot(223), plt.imshow(img, cmap='gray')
plt.title('Points Cloud'), plt.xticks([]), plt.yticks([])
plt.subplot(224), plt.imshow(coinImg)
plt.title('Image'), plt.xticks([]), plt.yticks([])
plt.show()

cv2.waitKey(0)
