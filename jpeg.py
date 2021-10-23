from pdf2image import convert_from_path
from os import mkdir


# например "Qj3z6UUuCic.pdf", "jpeg_files"
def pdf_to_jpeg(filename, save):
    pages = convert_from_path(filename, 500, poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
    try:
        mkdir(save)
    except Exception as e:
        print(e)
    for i in range(len(pages)):
        name = save + "\out" + str(i) + ".jpg"
        pages[i].save(name, 'JPEG')
