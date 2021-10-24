from django.http import Http404, HttpResponse
from django.shortcuts import render

from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
import secrets

from requests import request
import mimetypes


def index(request):



    # ЗАГРУЗКА ФАЙЛА НА СЕРВЕР
    if request.method == 'POST' and request.FILES['fidedrop_1']:
        
        # Генерация уникального ключа
        key = secrets.token_urlsafe(16)
        request.session['key'] = str(key)

        # Загрузка файла на сервер
        myfile = request.FILES['fidedrop_1']
        request.session['name'] = str(myfile)
        fs = FileSystemStorage()
        filename = fs.save(os.path.join(request.session.get('key'), myfile.name), myfile)
        uploaded_file_url = fs.url(filename)

        
        # ДЕБАГ
        return render(request, 'migrate/index.html', {
            'uploaded_file_url': uploaded_file_url,
        })
    return render(request, 'migrate/index.html')


def download(request):
    file_path = os.path.join(settings.MEDIA_URL, request.session.get('key'), request.session.get('name'))
    filename = 'out.pdf'

    fl = open(file_path, 'r')
    mime_type, _ = mimetypes.guess_type(file_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
