from django.http import Http404
from django.shortcuts import render

from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
import secrets

from requests import request

# ...
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
        
        # ДЕБАГ
        return render(request, 'migrate/index.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'migrate/index.html')