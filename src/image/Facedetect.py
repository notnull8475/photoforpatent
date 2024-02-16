import cv2

from src import Const


class FaceDetect:

    def __init__(self):
        # для определения центра лица
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
        # для определения центра глаз
        self.nested_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    def facedetect(self, img):
        def initialize_rolling_average_filter(x, y, w, h):
            return {'x': x, 'y': y, 'w': w, 'h': h}

        faces = self.face_cascade.detectMultiScale(img, 1.1, 4)

        new_x, new_y, new_w, new_h = 0, 0, 0, 0  # инициализация переменных
        if not self.nested_cascade.empty():
            for (x, y, w, h) in faces:
                # if prev_face is not None:
                #     prev_face = apply_rolling_average_filter(prev_face, {'x': x, 'y': y, 'w': w, 'h': h}, alpha)
                # else:

                prev_face = initialize_rolling_average_filter(x, y, w, h)
                x_center = prev_face['x'] + (prev_face['w'] / 2)
                y_center = prev_face['y'] + (prev_face['h'] / 2)

                new_w = int(prev_face['w'] * Const.face_rectangle_zoom)
                new_h = int(new_w * Const.ratio)

                new_x = int(x_center - (new_w / 2))
                new_y = int(y_center - new_h / 2)

                cv2.rectangle(img, (new_x, new_y), (new_x + new_w, new_y + new_h), (0,0,0), 2)

        face_sizes = {'x': new_x, 'y': new_y, 'w': new_w, 'h': new_h}
        return img,face_sizes

    def apply_rolling_average_filter(self, previous, current, alpha):
        filtered = {}
        for key in previous:
            filtered[key] = alpha * current[key] + (1 - alpha) * previous[key]
        return filtered
