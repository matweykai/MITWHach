from django.http import Http404, HttpResponse, FileResponse
from django.shortcuts import render

from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
import secrets

from requests import request
import mimetypes
import novus.pdf_work

def index(request):



    # ЗАГРУЗКА ФАЙЛА НА СЕРВЕР
    if request.method == 'POST' and request.FILES['filedrop_1'] and request.FILES['filedrop_2']:
        
        # Генерация уникального ключа
        key = secrets.token_urlsafe(16)
        request.session['key'] = str(key)

        # Загрузка файла на сервер
        myfile_1 = request.FILES['filedrop_1']
        request.session['name_1'] = str(myfile_1)
        fs_1 = FileSystemStorage()
        filename_1 = fs_1.save(os.path.join(request.session.get('key'), myfile_1.name), myfile_1)


        myfile_2 = request.FILES['filedrop_2']
        request.session['name_2'] = str(myfile_2)
        fs_2 = FileSystemStorage()
        filename_2 = fs_2.save(os.path.join(request.session.get('key'), myfile_2.name), myfile_2)

        target_path = os.getcwd().replace("\\", '/', os.getcwd().count("\\")) + f'/media/{key}'
        upd_file_path = novus.pdf_work.unit_file(target_path=target_path, file_names=(myfile_1, myfile_2))
        return FileResponse(open(upd_file_path, 'rb'))

        # ДЕБАГ
        # return render(request, 'migrate/index.html', {
        #     'uploaded_file_url': uploaded_file_url,
        # })
    return render(request, 'migrate/index.html')


def download(request):
    file_path = os.path.join(settings.MEDIA_URL, request.session.get('key'), request.session.get('name'))
    filename = 'out.pdf'

    fl = open(file_path, 'r')
    mime_type, _ = mimetypes.guess_type(file_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
