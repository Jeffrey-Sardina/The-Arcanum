import cv2
camera = cv2.VideoCapture(2)
while True:
    _, img = camera.read()
