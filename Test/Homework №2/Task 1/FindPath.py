import cv2
import math

points = []
pathLength: float = 0
scale = 3.2

img = cv2.imread("../../Resources/Map.png")
copyImg = img.copy()

def distance(a, b):
    return math.sqrt((math.pow(a[0] - b[0], 2) + (math.pow(a[1] - b[1], 2))))

def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY, pathLength, copyImg
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(copyImg, (x, y), 2, (255, 0, 0), -1)
        mouseX, mouseY = x, y
        points.append((x, y))
        if len(points) > 1:
            cv2.line(copyImg, points[len(points) - 1], points[len(points) - 2], (255, 0, 0), 2)
            pathLength += distance(points[len(points) - 1], points[len(points) - 2])

cv2.namedWindow('Map')
cv2.setMouseCallback('Map', draw_circle)

while True:
    cv2.imshow('Map', copyImg)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        cv2.putText(copyImg, f"{int(pathLength * scale)} meter", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    if key == ord('q'):
        break

cv2.waitKey(0)
