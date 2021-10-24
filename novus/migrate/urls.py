from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='migrate'),
    path('<str:filepath>/', views.download)
]