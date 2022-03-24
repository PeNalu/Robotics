import cv2
import numpy as np

img = cv2.imread("../../Resources/Color.png")
probability = 0.1


def getpixel(x, y, h, s, v, ratio):
    global img
    (h1, s1, v1) = img[x - 1, y]
    h += h1 / ratio
    s += s1 / ratio
    v += v1 / ratio
    return s, h, v


def onedimensionalwindow(x, y, img, width, ratio):
    h, s, v = img[x, y]
    h, s, v = h / ratio, s / ratio, v / ratio

    if x > 0:
        (h, s, v) = getpixel(x - 1, y, h, s, v, ratio)

    if x < width - 1:
        (h, s, v) = getpixel(x + 1, y, h, s, v, ratio)

    return h, s, v


def twodimensionalwindow(x, y, img, width, height, ratio):
    h, s, v = img[x, y]
    h, s, v = h / ratio, s / ratio, v / ratio

    if x > 0:
        (h, s, v) = getpixel(x - 1, y, h, s, v, ratio)

        if y < height - 1:
            (h, s, v) = getpixel(x - 1, y + 1, h, s, v, ratio)
            (h, s, v) = getpixel(x, y + 1, h, s, v, ratio)

        if y > 0:
            (h, s, v) = getpixel(x - 1, y - 1, h, s, v, ratio)
            (h, s, v) = getpixel(x, y - 1, h, s, v, ratio)

    if x < width - 1:
        (h, s, v) = getpixel(x + 1, y, h, s, v, ratio)

        if y > 0:
            (h, s, v) = getpixel(x + 1, y - 1, h, s, v, ratio)

        if y < height - 1:
            (h, s, v) = getpixel(x + 1, y + 1, h, s, v, ratio)

    return h, s, v

def sp_noise(image, prob):
    output = image.copy()
    if len(image.shape) == 2:
        black = 0
        white = 255
    else:
        colorspace = image.shape[2]
        if colorspace == 3:  # RGB
            black = np.array([0, 0, 0], dtype='uint8')
            white = np.array([255, 255, 255], dtype='uint8')
        else:  # RGBA
            black = np.array([0, 0, 0, 255], dtype='uint8')
            white = np.array([255, 255, 255, 255], dtype='uint8')
    probs = np.random.random(output.shape[:2])
    output[probs < (prob / 2)] = black
    output[probs > 1 - (prob / 2)] = white
    return output

while True:
    noiseImg = sp_noise(img, probability)
    copyNoiseImg = noiseImg.copy()
    cv2.putText(noiseImg, f"{int(probability * 100)} %", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("Noise", noiseImg)

    # (width, height) = noiseImg.shape[:2]
    # copyImg = noiseImg.copy()
    # for x in range(width):
    #     for y in range(height):
    #         copyImg[x, y] = twodimensionalwindow(x, y, copyNoiseImg, width, height, 9)
    #
    # (width, height) = noiseImg.shape[:2]
    # copyImg = noiseImg.copy()
    # for x in range(width):
    #     for y in range(height):
    #         copyImg[x, y] = onedimensionalwindow(x, y, copyNoiseImg, width, 5)
    #
    # copyImg = cv2.medianBlur(copyImg, 9)
    # copyImg = cv2.medianBlur(copyImg, 9)
    # cv2.imshow("My Filter", copyImg)

    blurImg = cv2.blur(copyNoiseImg, (5, 5))
    cv2.imshow("Blur", blurImg)

    gaussBlurImg = cv2.GaussianBlur(copyNoiseImg, (5, 5), cv2.BORDER_DEFAULT)
    cv2.imshow("GaussianBlur", gaussBlurImg)

    medianBlurImg = cv2.medianBlur(copyNoiseImg, 7)
    cv2.imshow("MedianBlur", medianBlurImg)

    bilateralImg = cv2.bilateralFilter(copyNoiseImg, 50, 10, 10)
    cv2.imshow("Bilateral", bilateralImg)

    probability += 0.1
    cv2.waitKey(2500)

    if probability > 0.9:
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
