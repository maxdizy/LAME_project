from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='MADI-home'),
    path('upload/', views.upload, name='MADI-upload'),
    path('createERF/', views.createERF, name='MADI-createERF'),
    path('createDART/', views.createDART, name='MADI-createDART'),
]