import cv2

video = cv2.VideoCapture(0)

frame_size = (int(video.get(3)), int(video.get(4)))
save = cv2.VideoWriter("Resources/video.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, frame_size)

while video.isOpened():
    res, img = video.read()
    save.write(img)
    cv2.imshow("Show", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

