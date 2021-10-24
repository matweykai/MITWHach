from django.urls import include, path

from . import views


urlpatterns = [
    path('delite/', include('delite.urls')),
    path('pdftojpg/', include('pdftojpg.urls')),
    path('rotate/', include('rotate.urls')),
    path('separate/', include('separate.urls')),
    path('migrate/', include('migrate.urls')),
    path('', views.index, name='index'),
]