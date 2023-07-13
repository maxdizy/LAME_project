from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
import random

joke = random.choice(open('data/jokes.txt', encoding="utf8").readlines())
joke = joke.split('<>')
hook = joke[0]
punch = joke[1]

urlpatterns = [
    path('', views.home, name='HOME-home'),
    path('planes/', views.planes, name='HOME-planes'),
    path('login/', auth_views.LoginView.as_view(template_name="HOME/login.html", extra_context={'hook' : hook, 'punch' : punch}), name='HOME-login'),
    path('contactAdmin/', views.contactAdmin, name='HOME-contactAdmin'),
    path('logout/', auth_views.LogoutView.as_view(template_name="HOME/logout.html", extra_context={'hook' : hook, 'punch' : punch}), name='HOME-logout'),
    path('profile/', views.profile, name='HOME-profile'),
]