import cv2

img = cv2.imread("Resources/Card.jpg")
photoSize = img.shape
photoCenter = (int(photoSize[1] / 2), int(photoSize[0] / 2))

rotateMatrix = cv2.getRotationMatrix2D(photoCenter, -180, 1)
image = cv2.warpAffine(img, rotateMatrix, (photoSize[1], photoSize[0]))

cv2.imshow("Rotate Image", image)
cv2.imshow("Source Image", img)
cv2.waitKey(0)

