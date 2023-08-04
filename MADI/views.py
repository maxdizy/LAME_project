import os
import random
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .MADI_config import readIRF, writeERF
from MADI.forms import uploadForm
from .models import config
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from LAME.settings import get_file, push_file

joke = random.choice(get_file('data/jokes.txt').read().decode().splitlines())
joke = joke.split('<>')
hook = joke[0]
punch = joke[1]

@login_required
def home(request):
    return render(request, 'MADI/home.html', {'form' : uploadForm, 'hook' : hook, 'punch' : punch, 'warning' : ''})

@login_required
def upload(request):
    if request.method == 'POST':
        form = uploadForm(request.POST, request.FILES)
        #does ERFpath exist or is writable?
        #if os.path.exists(request.POST.get("ERFpath")):
        if form.is_valid():
            form.save()
        push_file('data/ERFL.txt', request.POST.get("ERFpath"))
        global CN, tail, IRFTitle, description, affected, IRFNo, ROED, potROEDs, dart, mod, file
        CN, file, dart, mod = request.POST.get('caseNo'), request.FILES.get('file'), request.POST.get("dart"), request.POST.get("mod")
        tail, IRFTitle, description, affected, IRFNo, ROED, potROEDs = readIRF(file, CN)
        if ROED:
            return render(request, 'MADI/ROED.html', {'potROEDs' : potROEDs, 'hook' : hook, 'punch' : punch})
        # else:  
        #     writeERF(CN, tail, IRFTitle, description, affected, IRFNo, ROED, False, potROEDs, dart, mod, file.name)
        # else:
        #     return render(request, 'MADI/home.html', {'form' : uploadForm, 'hook' : hook, 'punch' : punch, 'warning' : 'ERROR: Some fields were not filled out correctly. Please make sure your ERF path is valid.'})
    return redirect('HOME-home')

@login_required
def createERF(request):
    writeERF(CN, tail, IRFTitle, description, affected, IRFNo, ROED, False, potROEDs, dart, mod, file.name)
    return redirect('HOME-home')
