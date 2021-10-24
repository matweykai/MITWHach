from pdf2image import convert_from_path
from os import mkdir, path


def pdf_to_jpeg(target_path, file_name, save):
    abs_folder = f'{target_path}/{save}'
    abs_file_name = f'{target_path}/{file_name}'
    if not path.exists(abs_folder):
        mkdir(abs_folder)
    try:
        pages = convert_from_path(abs_file_name, 70, poppler_path='../../poppler-0.68.0/bin')
        for i in range(len(pages)):
            name = abs_folder + "/out" + str(i) + ".jpg"
            pages[i].save(name, 'JPEG')
    except Exception as e:
        raise RuntimeError(f"Error during reading file {file_name}")
    return save


