from PyPDF2 import PdfFileReader as Reader

with open("Samples/Laboratornye_raboty_S.pdf", mode="rb") as file:
    reader = Reader(file)
    first_page = reader.getPage(0)
    first_page
    #text = reader.getFormTextFields()
    #print(type(text))
