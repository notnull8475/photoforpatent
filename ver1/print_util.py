from fpdf import FPDF
import cups
from tkinter.messagebox import showerror
from PIL import Image
import gui

def add_image(image_path, pdf_file):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.image(image_path, x=10, y=10, w=37, h=47)
    # pdf.set_font("Arial", size=12)
    # pdf.ln(85)  # ниже на 85
    # pdf.cell(200, 10, txt="{}".format(image_path), ln=1)
    pdf.output(pdf_file)


def print_image_with_cm_dimensions(image_path, width_cm, height_cm):
    try:
        conn = cups.Connection()
        printers = conn.getPrinters()

        printer_name = list(printers.keys())  # Replace with the actual printer name
        print(" список принтеров ", printer_name)
        gui.select_printer(printer_name)

        image = Image.open(image_path)
        dpi = 300  # Adjust the DPI based on the printer's capabilities
        width_px = int(width_cm / 2.54 * dpi)
        height_px = int(height_cm / 2.54 * dpi)
        resized_image = image.resize((width_px, height_px))
        resized_image.save("/tmp/resized_image.png")  # Save the resized image temporarily

        add_image("/tmp/resized_image.png", "/tmp/image.pdf")

        # conn.printFile(printer_name, "/tmp/image.pdf", "Image", {})  # Print the resized image
    except Exception as e:
        showerror(title="Ошибка", message=f"Не удалось напечатать изображение: {e}")
        print(f"An error occurred: {e}")


