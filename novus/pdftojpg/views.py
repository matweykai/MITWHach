from django.http import Http404, HttpResponse
from django.shortcuts import render

from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
import os
import secrets

from requests import request
import mimetypes
import novus.archivator
import novus.jpeg

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

        #=============================

        file_name = request.session.get('name')

        target_path = os.getcwd().replace("\\", '/', os.getcwd().count("\\")) + f'/media/{key}'

        upd_file_path = novus.jpeg.pdf_to_jpeg(target_path, file_name, 'img')
        archive = novus.archivator.archive_files(target_path, 'img')
        # Парсим и обрабатываем ошибки
        print("Form data resuved!")
        # key = request.session.get('key')
        # return render(request, 'delite/detail.html', {
        #     'key': key,
        #     'num' : request.POST.get('str_num'),
        #     'uploaded_file_url': "ТУТ ССЫЛКА НА ГОТОВЫЙ ФАЙЛ"
        # })
        return FileResponse(open(archive, 'rb'))

        #=============================

        # ДЕБАГ
        # return render(request, 'pdftojpg/index.html', {
        #     'uploaded_file_url': uploaded_file_url,
        # })
        
    return render(request, 'pdftojpg/index.html')