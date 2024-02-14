from tkinter import *
from tkinter import ttk
from src.image.Images import Images
import src.Const as Const


class Interface:

    def __init__(self, master):
        self.show_flag = True
        self.master = master
        self.imageFrame = ttk.Frame(master)  # создаем фрейм
        self.imageFrame.grid(row=0, column=0, columnspan=4)

        closeBtn = ttk.Button(text="Закрыть", command=self.finish)  # создаем кнопку
        closeBtn.grid(row=1, column=0)

        photoBtn = ttk.Button(text="Фото", command=lambda: self.take_snapshot)
        photoBtn.grid(row=1, column=1)

        saveBtn = ttk.Button(text="Сохранить", command=lambda: self.save_snapshot)
        saveBtn.grid(row=1, column=2)

        printBtn = ttk.Button(text="Печать", command=lambda: self.print_snapshot)
        printBtn.grid(row=1, column=3)

        # if self.show_flag:
        self.show_frame()


    def finish(self):
        self.master.destroy()  # ручное закрытие окна и всего приложения
        print("Закрытие приложения")

    def take_snapshot(self):
        pass

    def save_snapshot(self):
        pass

    def print_snapshot(self):
        pass

    def show_frame(self):
        l_main = ttk.Label(self.imageFrame)
        l_main.grid(row=0, column=0)
        images = Images
        # while self.show_flag:
        # print("показываю фрейм")
        imgtk = images.get_image()
        l_main.imgtk = imgtk
        l_main.configure(image=imgtk)
        if self.show_flag:
            l_main.after(Const.video_fps, self.show_frame())
