import random
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from LAME import settings

joke = random.choice(settings.get_file('data/jokes.txt').read().decode().splitlines())
joke = joke.split('<>')
hook = joke[0]
punch = joke[1]

def home(request):
    return render(request, 'HOME/home.html', {'hook' : hook, 'punch' : punch})

def planes(request):
    return render(request, 'HOME/planes.html')

def contactAdmin(request):
    return render(request, 'HOME/contactAdmin.html')

@login_required
def profile(request):
    return render(request, 'HOME/profile.html', {'hook' : hook, 'punch' : punch})
