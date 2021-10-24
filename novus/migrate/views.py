from django.shortcuts import render

from django.core.files.storage import FileSystemStorage
import requests
from django.http import FileResponse

import os
import secrets
# ...
import novus.pdf_work
import novus.archivator


def index(request):

    # ЗАГРУЗКА ФАЙЛА
    if request.method == 'POST' and request.FILES['fidedrop_1']:
        
        # Генерация уникального ключа
        key = secrets.token_urlsafe(16)
        request.session['key'] = str(key)


        # Загрузка файла на сервер
        myfile = request.FILES['fidedrop_1']
        fs = FileSystemStorage()
        filename = fs.save(os.path.join(request.session.get('key'), myfile.name), myfile)
        uploaded_file_url = fs.url(filename)

        request.session['file_name'] = myfile.name

        # ДЕБАГ
        return render(request, 'migrate/index.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'migrate/index.html')


def separate(request):
    key = request.session.get('key')
    t_path = os.path.join(os.getcwd(), f'/media/{key}')
    target_path = os.getcwd().replace("\\", '/', os.getcwd().count("\\")) + f'/media/{key}'

    file_name = request.session.get("file_name")

    folder_name = novus.pdf_work.split_file(target_path=target_path, file_name=file_name, split_points_indexes=(1, 3, 5))
    archived_file = novus.archivator.archive_files(target_path=target_path, folder_name=folder_name)

    return FileResponse(open(f'{archived_file}', 'rb'))
