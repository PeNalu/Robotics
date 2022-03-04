import cv2
import random
import string
import os
import shutil

images = []

img = cv2.imread("../../Resources/Card.jpg")
photoSize = img.shape

numberHeightSelection = random.randint(3, 6)
numberWidthSelection = random.randint(3, 6)

heightSection = photoSize[0] / numberHeightSelection
widthSelection = photoSize[1] / numberWidthSelection

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def drawphotopiece(minheight, maxheight, minwidth, maxwidth):
    newImg = img[int(minheight):int(maxheight), int(minwidth):int(maxwidth)]
    images.append((generate_random_string(5), newImg))

for i in range(0, numberHeightSelection):
    for j in range(0, numberWidthSelection):
        drawphotopiece(i * heightSection, heightSection * (i + 1), j * widthSelection, widthSelection * (j + 1))

while True:
    for name, image in images:
        cv2.imshow(name, image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../PhotoPart')
        shutil.rmtree(path)
        os.mkdir("../../PhotoPart")
        for i, (name, image) in enumerate(images):
            cv2.imwrite(f"PhotoPart/{str(i)}.jpg", image)
        break

cv2.destroyAllWindows()
