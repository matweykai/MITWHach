import PyPDF2
from PyPDF2 import utils
from os import mkdir, path
from django.http import FileResponse


# target_path - папка пользователя относительно текущей директории


def rotate_file(target_path, file_name, page_indexes, degrees):
    """
    Function which rotate pages contains in page_index pivot by the values specified in the array degrees
    :param target_path: name of user folder
    :param file_name: file for changes
    :param page_indexes: indexes of pages for rotations
    :param degrees: values for rotations
    :return: changed file
    """
    file_name = f'{target_path}/{file_name}'
    new_file_name = f'{target_path}/Rotated_File.pdf'
    with open(file_name, 'rb') as pdf_file, open(new_file_name, 'wb') as pdf_file_rotated:
        try:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        except utils.PdfReadError:
            raise RuntimeError(f"Error during reading file {file_name}")
        pdf_writer = PyPDF2.PdfFileWriter()
        for page_num in range(pdf_reader.numPages):
            pdf_page = pdf_reader.getPage(page_num)
            if page_num in page_indexes:
                pdf_page.rotateClockwise(degrees[page_indexes.index(page_num)])  # rotateCounterClockwise()
            pdf_writer.addPage(pdf_page)
        pdf_writer.write(pdf_file_rotated)
    return new_file_name


def unit_file(target_path, file_names):
    """
    Function for union files
    :param target_path: name of user folder
    :param file_names: files for union
    :return: new merged file
    """
    new_file_name = f'{target_path}/Unit_file.pdf'
    pdf_merger = PyPDF2.PdfFileMerger()
    for file_name in file_names:
        pdf_file_name = f'{target_path}/{file_name}'
        try:
            pdf_merger.append(PyPDF2.PdfFileReader(pdf_file_name, strict=False))
        except utils.PdfReadError:
            raise RuntimeError(f"Error during reading file {file_name}")
    with open(new_file_name, 'wb') as pdf_file_merged:
        pdf_merger.write(pdf_file_merged)
    return new_file_name


def split_file(target_path, file_name, split_points_indexes):
    """
    Function for splitting file according to indexes in split_points_indexes
    :param target_path: name of user folder
    :param file_name: file for changes
    :param split_points_indexes: indexes for splitting
    :return: folder which contains split files
    """
    abs_file_name = f'{target_path}/{file_name}'
    folder = 'split_files'
    abs_folder = f'{target_path}/split_files'

    with open(abs_file_name, 'rb') as pdf_file:
        try:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        except utils.PdfReadError:
            raise RuntimeError(f"Error during reading file {file_name}")
        split_points_indexes = sorted(split_points_indexes)
        split_points_indexes.insert(0, 0)
        split_points_indexes.append(pdf_reader.numPages)
        if not path.exists(abs_folder):
            mkdir(abs_folder)
        file_index = 0
        for i, j in zip(split_points_indexes[:-1], split_points_indexes[1:]):
            pdf_writer = PyPDF2.PdfFileWriter()
            for page_num in range(i, j):
                pdf_writer.addPage(pdf_reader.getPage(page_num))
            file_index += 1
            new_file_name = f'{abs_folder}/{file_name[:-4]}_{file_index}.pdf'
            with open(new_file_name, 'wb') as output_file:
                pdf_writer.write(output_file)
    return folder


def delete_pages(target_path, file_name, page_indexes):
    """
    Function for deleting pages indexes of which contains in page_indexes
    :param target_path: name of user folder
    :param file_name: file for changing
    :param page_indexes: page numbers to be deleted
    :return: changed file
    """
    abs_file_name = f'{target_path}/{file_name}'
    new_file_name = f'{target_path}/File_Without_Some_Pages.pdf'
    with open(abs_file_name, 'rb') as pdf_file:
        try:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        except utils.PdfReadError:
            raise RuntimeError(f"Error during reading file {file_name}")
        pdf_writer = PyPDF2.PdfFileWriter()
        add = pdf_writer.addPage
        for page_num in range(pdf_reader.numPages):
            if (page_num + 1) not in page_indexes:
                add(pdf_reader.getPage(page_num))
        with open(new_file_name, 'wb') as output_file:
            pdf_writer.write(output_file)
    return new_file_name


def send_file_to_user(file_path):
    return FileResponse(open(file_path, 'rb'))
