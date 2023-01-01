from fpdf import FPDF
from PIL import Image
import os
import time

WIDTH = 595
HEIGHT = 421


def image_compose(image_1, image_2):
    first = Image.open(image_1).resize((WIDTH - 100, HEIGHT - 100), Image.ANTIALIAS)
    second = Image.open(image_2).resize((WIDTH - 100, HEIGHT - 100), Image.ANTIALIAS)
    new_image = Image.new('RGB', (WIDTH, HEIGHT * 2), (255, 255, 255))
    new_image.paste(first, (50, 50))
    new_image.paste(second, (50, HEIGHT + 50))
    return new_image


def make_pdf(pdfFileName, listPages):
    pdf = FPDF(unit="pt", format=[WIDTH, HEIGHT * 2])
    end = len(listPages)
    for index in range(0, end, 2):
        pdf.add_page()
        if index + 1 is not end:
            image_compose(listPages[index], listPages[index + 1]).save("./tmp/%d.jpg" % index)
            pdf.image("./tmp/%d.jpg" % index, 0, 0)

        else:
            pdf.image(listPages[index], 0, 0)

    pdf.output(pdfFileName, "F")


def func():
    image_dir_path = './imgs/'
    images = [os.path.join(image_dir_path, imgFileName) for imgFileName in os.listdir(image_dir_path)]
    make_pdf("./tmp/imgs.pdf", images)


# def main():
#     func()
#
#
# if __name__ == '__main__':
#     main()
