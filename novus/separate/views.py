from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage

import os
import secrets

from requests import request
import mimetypes
import novus.pdf_work
import novus.archivator


def index(request):
    
    uploaded = False # флаг

    # РЕДИРЕКТ НА ФОРМУ НАСТРОЙКИ С СЫЛКОЙ НА СКАЧКУ
    if request.method == 'POST' and request.session.get('key') and request.POST.get('str_num'):
        print("Form data resuved!")
        key = request.session.get('key')
        file_name = request.session.get('name')
        # str_num

        received_data = request.POST.get('str_num')
        # Проверка на пустоту, на числа и могут быть отрицательны числа или больше чем кол-во страниц
        page_nums_list = list((int(num_s) for num_s in received_data.split(',') if num_s != ''))

        target_path = os.getcwd().replace("\\", '/', os.getcwd().count("\\")) + f'/media/{key}'

        upd_file_path = novus.pdf_work.split_file(target_path=target_path, file_name=file_name, split_points_indexes=page_nums_list)
        archived_file_path = novus.archivator.archive_files(target_path, upd_file_path)

        return FileResponse(open(archived_file_path, 'rb'))


    #     return render(request, 'separate/detail.html', {
    #         'key': key,
    #         'num' : request.POST.get('str_num'),
    #         'uploaded_file_url': "ТУТ ССЫЛКА НА ГОТОВЫЙ ФАЙЛ"
    # })

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
        return render(request, 'separate/detail.html', {
            'key': key,
        })
        
    return render(request, 'separate/index.html')
