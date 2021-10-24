from django.shortcuts import render

from django.core.files.storage import FileSystemStorage

import os
import secrets
# ...
import novus.pdf_work


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
    target_path = os.getcwd().replace("\\", '/', os.getcwd().count("\\")) + f'/media/{key}'
    file_name = request.session.get("file_name")

    novus.pdf_work.split_file(target_path=target_path, file_name=file_name, split_points_indexes=(1, 3, 5))

    return
