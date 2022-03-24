import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("../../Resources/Card.jpg", 0)
probability = 0.2

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

def ConvertToFrequencySpace(imgToConvert):
    raw_img = (imgToConvert / 255.0) * 2.0 - 1.0
    raw_img = np.flipud(raw_img)
    rms = 0.2

    raw_img = raw_img - np.mean(raw_img)
    raw_img = raw_img / np.std(raw_img)
    raw_img = raw_img * rms

    img_freq = np.fft.fft2(raw_img)
    img_amp = np.fft.fftshift(np.abs(img_freq))
    img_amp_disp = np.log(img_amp + 0.0001)
    img_amp_disp = (
                           (
                                   (img_amp_disp - np.min(img_amp_disp)) * 2
                           ) / np.ptp(img_amp_disp)
                   ) - 1

    return img_amp_disp

probability = float(input('Enter probabilitye: (Example 0.4)'))

noiseImg = sp_noise(img, probability)
copyNoiseImg = noiseImg.copy()
cv2.putText(noiseImg, f"{int(probability * 100)} %", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

frequencySpaceImage = ConvertToFrequencySpace(copyNoiseImg)

f = np.fft.fft2(copyNoiseImg)
fshift = np.fft.fftshift(f)
rows, cols = img.shape[:2]
crow, ccol = rows // 2, cols // 2
magnitude_spectrum = 20 * np.log(np.abs(fshift))
fshift[crow - 30:crow + 31, ccol - 30:ccol + 31] = 0
f_ishift = np.fft.ifftshift(fshift)
img_back = np.fft.ifft2(f_ishift)
img_back = np.real(img_back)

img_back_copy = img_back.copy()

dft = cv2.dft(np.float32(copyNoiseImg), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

mask = np.zeros((rows, cols, 2), np.uint8)
mask[crow - 30:crow + 30, ccol - 30:ccol + 30] = 1
fshift = dft_shift * mask
f_ishift = np.fft.ifftshift(fshift)
img_back = cv2.idft(f_ishift)
img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

plt.subplot(221), plt.imshow(copyNoiseImg, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(222), plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.subplot(223), plt.imshow(img_back, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.subplot(224), plt.imshow(img_back_copy)
plt.title('Result in JET'), plt.xticks([]), plt.yticks([])

plt.show()

mean_filter = np.ones((3, 3))
x = cv2.getGaussianKernel(5, 10)
gaussian = x*x.T
scharr = np.array([[-3, 0, 3],
                   [-10, 0, 10],
                   [-3, 0, 3]])
sobel_x = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])
sobel_y = np.array([[-1, -2, -1],
                   [0, 0, 0],
                   [1, 2, 1]])
laplacian = np.array([[0, 1, 0],
                    [1, -4, 1],
                    [0, 1, 0]])
filters = [mean_filter, gaussian, laplacian, sobel_x, sobel_y, scharr]
filter_name = ['mean_filter', 'gaussian','laplacian', 'sobel_x', \
                'sobel_y', 'scharr_x']
fft_filters = [np.fft.fft2(x) for x in filters]
fft_shift = [np.fft.fftshift(y) for y in fft_filters]
mag_spectrum = [np.log(np.abs(z)+1) for z in fft_shift]
for i in range(6):
    plt.subplot(2, 3, i+1), plt.imshow(mag_spectrum[i], cmap = 'gray')
    plt.title(filter_name[i]), plt.xticks([]), plt.yticks([])
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()