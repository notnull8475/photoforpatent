from tkinter import *
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter import filedialog
import cv2

import print_util

aspect_ratio = 4.5 / 3.5
rectangle_color = (255, 255, 255)
image_size_ratio = 1.5
prev_face = None
alpha = 0.2
image = None
image_sizes = None
photo_flag = True
image_path = None
video_port = 0


def finish():
    root.destroy()  # ручное закрытие окна и всего приложения
    print("Закрытие приложения")


def print_snapshot():
    global image_path
    if image_path is not None:
        print_util.print_image_with_cm_dimensions(image_path,3.7, 4.7)
    else:
        showwarning(title="Предупреждение", message="Необходимо сохранить фото")
    print("Печать")





# Example usage


def save_snapshot():
    global image_sizes, image_path, image
    if image is not None:
        if image_sizes is not None:
            image = image.crop((image_sizes['x'], image_sizes['y'], image_sizes['x'] + image_sizes['w'],
                                image_sizes['y'] + image_sizes['h']))
            image_sizes = None
        rgb_im = image.convert('RGB')
        file = filedialog.asksaveasfilename(title="Сохранить", defaultextension=".jpg",
                                            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"),
                                                       ("All Files", "*.*")])
        if file:
            image_path = file
            rgb_im.save(file)
        else:
            take_snapshot()
            save_snapshot()
    else:
        showerror(title="Ошибка", message="Не удалось сохранить изображение")
        print("Не удалось сохранить изображение")


def take_snapshot():
    global photo_flag
    if photo_flag:
        photo_flag = False
    else:
        photo_flag = True
        show_frame()


# def crop_image(image, x, y, width, height):
def crop_image(img, a):
    cropped_image = img.crop((a['x'], a['y'], a['x'] + a['w'], a['y'] + a['h']))
    return cropped_image


def apply_rolling_average_filter(previous, current, alpha):
    filtered = {}
    for key in previous:
        filtered[key] = alpha * current[key] + (1 - alpha) * previous[key]
    return filtered


def initialize_rolling_average_filter(x, y, w, h):
    return {'x': x, 'y': y, 'w': w, 'h': h}


def show_frame():
    global image
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    facedetect(cv2image)
    image = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=image)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if photo_flag:
        lmain.after(10, show_frame)
    # lmain.after(100, show_frame)


def facedetect(img):
    global prev_face, image_sizes
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    nested_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    new_x, new_y, new_w, new_h = 0, 0, 0, 0
    if not nested_cascade.empty():
        for (x, y, w, h) in faces:
            # if prev_face is not None:
            #     prev_face = apply_rolling_average_filter(prev_face, {'x': x, 'y': y, 'w': w, 'h': h}, alpha)
            # else:
            prev_face = initialize_rolling_average_filter(x, y, w, h)
            x_center = prev_face['x'] + (prev_face['w'] / 2)
            y_center = prev_face['y'] + (prev_face['h'] / 2)

            new_w = int(prev_face['w'] * image_size_ratio)
            new_h = int(new_w * aspect_ratio)

            new_x = int(x_center - (new_w / 2))
            new_y = int(y_center - new_h / 2)

            cv2.rectangle(img, (new_x, new_y), (new_x + new_w, new_y + new_h), rectangle_color, 2)

    image_sizes = {'x': new_x, 'y': new_y, 'w': new_w, 'h': new_h}


root = Tk()  # создаем корневой объект - окно
root.title("PhotoBooth")  # устанавливаем заголовок окна
# root.geometry("800x600+400+200")  # устанавливаем размеры окна


imageFrame = ttk.Frame(root, width=1280, height=1080)  # создаем фрейм
imageFrame.grid(row=0, column=0, columnspan=4)

closeBtn = ttk.Button(text="Закрыть", command=finish)  # создаем кнопку
closeBtn.grid(row=1, column=0)

photoBtn = ttk.Button(text="Фото", command=lambda: take_snapshot())
photoBtn.grid(row=1, column=1)

saveBtn = ttk.Button(text="Сохранить", command=lambda: save_snapshot())
saveBtn.grid(row=1, column=2)

printBtn = ttk.Button(text="Печать", command=lambda: print_snapshot())
printBtn.grid(row=1, column=3)

lmain = ttk.Label(imageFrame)
lmain.grid(row=0, column=0)
cap = cv2.VideoCapture(video_port)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # Включение автофокуса

show_frame()

root.mainloop()
