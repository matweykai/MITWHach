from django.http import Http404, HttpResponse
from django.shortcuts import render

from django.core.files.storage import FileSystemStorage

import os
import secrets

from requests import request
import mimetypes


def index(request):
    
    uploaded = False # флаг

    # РЕДИРЕКТ НА ФОРМУ НАСТРОЙКИ С СЫЛКОЙ НА СКАЧКУ
    if request.method == 'POST' and request.session.get('key') and request.POST.get('str_num'):
        print("Form data resuved!")
        key = request.session.get('key')
        return render(request, 'rotate/detail.html', {
            'key': key,
            'num' : request.POST.get('str_num'),
            'angle': request.POST.get('str_angle'),
            'uploaded_file_url': "ТУТ ССЫЛКА НА ГОТОВЫЙ ФАЙЛ"
    })

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

        # РЕДИРЕКТ НА ФОРМУ НАСТРОЙКИ
        return render(request, 'rotate/detail.html', {
            'key': key,
        })
        
    return render(request, 'rotate/index.html')
