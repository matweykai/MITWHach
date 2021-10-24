from django.http import Http404, HttpResponse
from django.shortcuts import render

from django.core.files.storage import FileSystemStorage

import os
import secrets

from requests import request
import mimetypes

# Create your views here.
def index(request):


    uploaded = False

    # ЗАГРУЗКА ФАЙЛА НА СЕРВЕР
    if request.method == 'POST' and request.FILES['fidedrop_1'] and not uploaded:
        
        # Генерация уникального ключа
        key = secrets.token_urlsafe(16)
        request.session['key'] = str(key)

        # Загрузка файла на сервер
        myfile = request.FILES['fidedrop_1']
        request.session['name'] = str(myfile)
        fs = FileSystemStorage()
        filename = fs.save(os.path.join(request.session.get('key'), myfile.name), myfile)
        uploaded_file_url = fs.url(filename)
        uploaded = True

        # ДЕБАГ
        return render(request, 'pdftojpg/index.html', {
            'uploaded_file_url': uploaded_file_url,
        })
        
    return render(request, 'pdftojpg/index.html')