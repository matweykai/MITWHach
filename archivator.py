import os
import zipfile


# #exapmle how to use
# name_address_output_zip = 'C:\\Users\\mrtik\\PycharmProjects\\hack.zip'
# where_files_live = 'C:\\Users\\mrtik\\PycharmProjects\\HACK'
# archive_files(name_address_output_zip, where_files_live)


def archive_files(name_address_output_zip, where_files_live):
    fantasy_zip = zipfile.ZipFile(name_address_output_zip, 'w')
    try:
        for folder, subfolders, files in os.walk(where_files_live):

            for file in files:
                fantasy_zip.write(os.path.join(folder, file),
                                  os.path.relpath(os.path.join(folder, file), where_files_live),
                                  compress_type=zipfile.ZIP_DEFLATED)
    except IOError as e:
        print(u'не удалось открыть файл')
        print(e)
    finally:
        fantasy_zip.close()
