from django.http import Http404, HttpResponse
from django.shortcuts import render

from django.core.files.storage import FileSystemStorage
from django.http import FileResponse

import os
import secrets

from requests import request
import mimetypes
import novus.pdf_work
import novus.jpeg
from shutil import move


# Create your views here.
def index(request):
    
    uploaded = False # флаг

    # РЕДИРЕКТ НА ФОРМУ НАСТРОЙКИ С СЫЛКОЙ НА СКАЧКУ
    if request.method == 'POST' and request.session.get('key') and request.POST.get('str_num'):

        # Прилетели данные в виде строки
        # str_num - данные из формы
        key = request.session.get('key')
        file_name = request.session.get('name')
        received_data = request.POST.get('str_num')
        # Проверка на пустоту, на числа и могут быть отрицательны числа или больше чем кол-во страниц
        page_nums_list = list((int(num_s) for num_s in received_data.split(',') if num_s != ''))

        target_path = os.getcwd().replace("\\", '/', os.getcwd().count("\\")) + f'/media/{key}'

        upd_file_path = novus.pdf_work.delete_pages(target_path=target_path, file_name=file_name, page_indexes=page_nums_list)

        # Парсим и обрабатываем ошибки
        print("Form data resuved!")
        # key = request.session.get('key')
        # return render(request, 'delite/detail.html', {
        #     'key': key,
        #     'num' : request.POST.get('str_num'),
        #     'uploaded_file_url': "ТУТ ССЫЛКА НА ГОТОВЫЙ ФАЙЛ"
        # })
        return FileResponse(open(upd_file_path, 'rb'))


    # ЗАГРУЗКА ФАЙЛА НА СЕРВЕР
    if request.method == 'POST' and request.FILES['filedrop_1'] and not uploaded:
        
        # Генерация уникального ключа
        key = secrets.token_urlsafe(16)
        request.session['key'] = str(key)

        target_path = os.getcwd().replace("\\", '/', os.getcwd().count("\\")) + f'/media/{key}'
        # Загрузка файла на сервер
        myfile = request.FILES['filedrop_1']
        request.session['name'] = str(myfile)
        fs = FileSystemStorage()
        filename = fs.save(os.path.join(request.session.get('key'), myfile.name), myfile)
        uploaded_file_url = fs.url(filename)
        uploaded = True

        #SEND IMG======
        folder_path = novus.jpeg.pdf_to_jpeg(target_path, request.session.get('name'), "img")
        imges_path = os.getcwd().replace("\\", '/', os.getcwd().count("\\")) + f'/delite/static/img/{key}'

        img_count = len(os.listdir(folder_path))

        os.mkdir(imges_path)
        move(folder_path, imges_path)

        src = []
        for i in range(0, img_count):
            src.append('out'+str(i))


        # РЕДИРЕКТ НА ФОРМУ НАСТРОЙКИ
        return render(request, 'delite/detail.html', {
            'key': key,
            'src': src,
        })
    return render(request, 'delite/index.html')

    