from flask import flash

import cv2

def get_camera():
    return cv2.VideoCapture(0)

def capture_image():
    cam = get_camera()
    ret, frame = cam.read()
    cam.release()
    if ret:
        image_path = 'captured_image.jpg'
        cv2.imwrite(image_path, frame)
        return image_path
    else:
        flash('Failed to capture image from camera.')
        return None