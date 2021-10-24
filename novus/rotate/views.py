from django.http import Http404, HttpResponse
from django.shortcuts import render

from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from shutil import move

import os
import secrets

from requests import request
import mimetypes
import novus.pdf_work


def index(request):
    
    uploaded = False # флаг

    # РЕДИРЕКТ НА ФОРМУ НАСТРОЙКИ С СЫЛКОЙ НА СКАЧКУ
    if request.method == 'POST' and request.session.get('key') and request.POST.get('str_num') and request.POST.get('str_angle'):
        key = request.session.get('key')

        # Проверка на пустоту, на числа и могут быть отрицательны числа или больше чем кол-во страниц

        recieved_pages = list((int(page_num) - 1 for page_num in request.POST.get('str_num').split(',')))
        recived_degrees = list((int(page_num) for page_num in request.POST.get('str_angle').split(',')))

        file_name = request.session.get('name')
        target_path = os.getcwd().replace("\\", '/', os.getcwd().count("\\")) + f'/media/{key}'

        upd_file_path = novus.pdf_work.rotate_file(target_path=target_path, file_name=file_name,
                                                   page_indexes=recieved_pages, degrees=recived_degrees)
        return FileResponse(open(upd_file_path, 'rb'))

    # ЗАГРУЗКА ФАЙЛА НА СЕРВЕР
    if request.method == 'POST' and request.FILES['filedrop_1'] and not uploaded:
        
        # Генерация уникального ключа
        key = secrets.token_urlsafe(16)
        request.session['key'] = str(key)

        # Загрузка файла на сервер
        myfile = request.FILES['filedrop_1']
        request.session['name'] = str(myfile)
        fs = FileSystemStorage()
        filename = fs.save(os.path.join(request.session.get('key'), myfile.name), myfile)
        uploaded_file_url = fs.url(filename)
        uploaded = True

        target_path = os.getcwd().replace("\\", '/', os.getcwd().count("\\")) + f'/media/{key}'
        folder_path = novus.jpeg.pdf_to_jpeg(target_path, request.session.get('name'), "img")
        imges_path = os.getcwd().replace("\\", '/', os.getcwd().count("\\")) + f'/rotate/static/img/{key}'

        img_count = len(os.listdir(folder_path))

        os.mkdir(imges_path)
        move(folder_path, imges_path)

        src = []
        for i in range(0, img_count):
            src.append('out' + str(i))

        # РЕДИРЕКТ НА ФОРМУ НАСТРОЙКИ
        return render(request, 'rotate/detail.html', {
            'key': key,
            'src': src,
        })
        
    return render(request, 'rotate/index.html')
