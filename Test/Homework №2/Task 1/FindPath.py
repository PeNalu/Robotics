import cv2
import math

points = []
pathLength: float = 0
scale: float = 3.2
endDrawing: bool = False

img = cv2.imread("../../Resources/Map.png")


def distance(a, b):
    return math.sqrt((math.pow(a[0] - b[0], 2) + (math.pow(a[1] - b[1], 2))))


def draw_circle(event, x, y, flags, param):
    global pathLength, img

    if endDrawing:
        return

    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), 2, (0, 255, 0), -1)
        points.append((x, y))

        if len(points) > 1:
            cv2.line(img, points[len(points) - 1], points[len(points) - 2], (0, 0, 255), 2)
            pathLength += distance(points[len(points) - 1], points[len(points) - 2])


cv2.namedWindow('Map')
cv2.setMouseCallback('Map', draw_circle)

while True:
    cv2.imshow('Map', img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        if not endDrawing:
            cv2.putText(img, f"{int(pathLength * scale)} meter", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 144, 144), 2, cv2.LINE_AA)

            endDrawing = True

    if key == ord('q'):
        break

cv2.waitKey(0)
