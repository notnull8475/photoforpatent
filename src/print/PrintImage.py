import tkinter
from tkinter import *
from tkinter import ttk

import cups

import src.Const as Const


class PrintImage:

    def __init__(self):
        pass

    def getPrinters(self):
        conn = cups.Connection()
        printers = conn.getPrinters()
        return list(printers)

    def showPrintForm(self, master):
        window = tkinter.Toplevel()
        window.title("Выбор принтера")
        select_printer = tkinter.StringVar
        print_menu = ttk.Combobox(window, textvariable=select_printer, values=self.getPrinters())
        print_menu.grid(row=0, column=0)

    def showImageToPrint(self, master, image):
        imageWindow = tkinter.Toplevel()
        imageWindow.title("Изображение для печати")
        label = tkinter.Label(imageWindow)
        label.grid(row=0, column=0, columnspan=3)
        printButton = tkinter.Button(imageWindow, text="Печать", command=lambda: self.printImage(image))
        printerSelectButton = tkinter.Button(imageWindow, text="Выбрать принтер",
                                             command=lambda: self.showPrintForm(master))
        cancelButton = tkinter.Button(imageWindow, text="Отмена", command=lambda: imageWindow.destroy())
        printButton.grid(row=1, column=0)
        printerSelectButton.grid(row=1, column=1)
        cancelButton.grid(row=1, column=2)
        from PIL import ImageTk
        imgtk = ImageTk.PhotoImage(image)

        label.imgtk = imgtk
        label.configure(image=imgtk)
        pass

    def printImage(self, image):
        pass
