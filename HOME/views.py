import random
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from LAME.settings import get_file

joke = random.choice(get_file('data/jokes.txt').read().decode().splitlines())
joke = joke.split('<>')
hook = joke[0]
punch = joke[1]

def home(request):
    return render(request, 'HOME/home.html', {'hook' : hook, 'punch' : punch})

def planes(request):
    return render(request, 'HOME/planes.html', {'hook' : hook, 'punch' : punch})

def contactAdmin(request):
    return render(request, 'HOME/contactAdmin.html', {'hook' : hook, 'punch' : punch})

@login_required
def profile(request):
    return render(request, 'HOME/profile.html', {'hook' : hook, 'punch' : punch})
