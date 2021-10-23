import os
import zipfile


# #exapmle how to use
# name_address_output_zip = 'C:\\Users\\mrtik\\PycharmProjects\\hack.zip'
# where_files_live = 'C:\\Users\\mrtik\\PycharmProjects\\HACK'
# archive_files(name_address_output_zip, where_files_live)


def archive_files(target_path, file_name):
    name_address_output_zip = f'{target_path}/My_Zip.zip'
    abs_file_name = f'{target_path}/{file_name}'
    fantasy_zip = zipfile.ZipFile(name_address_output_zip, 'w')
    try:
        for folder, subfolders, files in os.walk(abs_file_name):
            for file in files:
                fantasy_zip.write(os.path.join(folder, file),
                                  os.path.relpath(os.path.join(folder, file), target_path),
                                  compress_type=zipfile.ZIP_DEFLATED)
    except Exception:
        raise RuntimeError(f"Error during reading file {file_name}")
    finally:
        fantasy_zip.close()
