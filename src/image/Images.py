import cv2
import src.Const as Const
from PIL import Image, ImageTk

from src.image.Facedetect import FaceDetect


class Images:

    def __init__(self):
        print("Инициализация видео")
        self.cap = cv2.VideoCapture(Const.video_port)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # Включение автофокуса
        self.facedetect = FaceDetect()

    def get_image(self):
        _, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        cv2image, face_size = self.facedetect.facedetect(cv2image)
        image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=image)
        return cv2image, image, imgtk, face_size

    def crop_image(self, face_size, img):
        if face_size is not None:
            return img.crop(
                (face_size['x'], face_size['y'], face_size['x'] + face_size['w'], face_size['y'] + face_size['h']))
        else:
            return img
