from fpdf import FPDF


def add_image(image_path, pdf_file):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.image(image_path, x=10, y=10, w=37, h=47)
    # pdf.set_font("Arial", size=12)
    # pdf.ln(85)  # ниже на 85
    # pdf.cell(200, 10, txt="{}".format(image_path), ln=1)
    pdf.output(pdf_file)
