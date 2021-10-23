import PyPDF2


def rotate_file(target_path, file_name, page_indexes, degrees):
    file_name = f'{target_path}/{file_name}'
    new_file_name = f'{target_path}/Rotated_File.pdf'
    with open(file_name, 'rb') as pdf_file, open(new_file_name, 'wb') as pdf_file_rotated:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_writer = PyPDF2.PdfFileWriter()
        for page_num in range(pdf_reader.numPages):
            pdf_page = pdf_reader.getPage(page_num)
            if page_num in page_indexes:
                pdf_page.rotateClockwise(degrees[page_indexes.index(page_num)])  # rotateCounterClockwise()
            pdf_writer.addPage(pdf_page)
        pdf_writer.write(pdf_file_rotated)
    return new_file_name
