from tkinter import *
from tkinter import ttk
from src.image.Images import Images
from src.print.PrintImage import PrintImage
import src.Const as Const


class Interface:

    def __init__(self, master):
        self.show_flag = True
        self.master = master
        self.face = Face()
        self.imageFrame = ttk.Frame(master)  # создаем фрейм
        self.imageFrame.grid(row=0, column=0, columnspan=5)

        settingsBtn = ttk.Button(text="Настройки")
        settingsBtn.grid(row=1, column=0)
        closeBtn = ttk.Button(text="Закрыть", command=self.finish)  # создаем кнопку
        closeBtn.grid(row=1, column=1)

        photoBtn = ttk.Button(text="Фото", command=lambda: self.take_snapshot())
        photoBtn.grid(row=1, column=2)

        saveBtn = ttk.Button(text="Сохранить", command=lambda: self.save_snapshot())
        saveBtn.grid(row=1, column=3)

        printBtn = ttk.Button(text="Печать", command=lambda: self.print_snapshot())
        printBtn.grid(row=1, column=4)

        self.l_main = ttk.Label(self.imageFrame)
        self.l_main.grid(row=0, column=0)

        self.images = Images()
        self.printer = PrintImage()
        print("Инициализация видео в интерфйсе")

        # if self.show_flag:
        self.show_frame()

    def finish(self):
        self.master.destroy()  # ручное закрытие окна и всего приложения
        print("Закрытие приложения")

    def take_snapshot(self):
        if self.show_flag:
            self.show_flag = False
            return
        else:
            self.show_flag = True
            self.show_frame()

    def save_snapshot(self):
        print("сохраняю фото")
        self.show_flag = False
        if self.face.image is None:
            self.show_flag = True
            return
        else:
            self.face.face_image = self.images.crop_image(self.face.sizes, self.face.image)
            rgb_im = self.face.face_image.convert('RGB')
            from tkinter import filedialog
            file = filedialog.asksaveasfilename(title="Сохранить", defaultextension=".jpg",
                                            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"),
                                                       ("All Files", "*.*")])
            if file:
                self.face.path = file
                rgb_im.save(file)
            else:
                self.show_flag = True
                return

    def print_snapshot(self):
        print("печатаю фото")
        if self.face.image is not None:
            self.printer.showImageToPrint(self.master, self.face.face_image)
        pass

    def show_frame(self):
        cv2image, image, imgtk, face_size = self.images.get_image()
        self.l_main.imgtk = imgtk
        self.l_main.configure(image=imgtk)
        if self.show_flag:
            self.l_main.after(Const.video_fps, self.show_frame)
        else:
            self.face.sizes = face_size
            self.face.image = image

    # def set_photo
#

class Face:
    sizes = {'x': None, 'y': None, 'w': None, 'h': None}
    image = None
    face_image = None
    path = None
