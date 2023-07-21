import os
import random
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .MADI_config import readIRF, writeERF
from MADI.forms import uploadForm
from MADI.forms import IRFdataForm
from .models import config
from .models import IRFdata
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from LAME.settings import get_file, push_file

joke = random.choice(get_file('data/jokes.txt').read().decode().splitlines())
joke = joke.split('<>')
hook = joke[0]
punch = joke[1]

@login_required
@csrf_exempt
def home(request):
    return render(request, 'MADI/home.html', {'form' : uploadForm, 'hook' : hook, 'punch' : punch, 'warning' : ''})

@login_required
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        form = uploadForm(request.POST, request.FILES)
        #does ERFpath exist or is writable?
        if os.path.exists(request.POST.get("ERFpath")) or os.access(os.path.dirname(request.POST.get("ERFpath")), os.W_OK):
            if form.is_valid():
                form.save()
            request.user.first_name = "paul"
            push_file('data/ERFL.txt', request.POST.get("ERFpath"))
            global CN, tail, IRFTitle, description, affected, IRFNo, ROED, potROEDs, dart, mod, file
            CN, file, dart, mod = request.POST.get('caseNo'), request.FILES.get('file'), request.POST.get("dart"), request.POST.get("mod")
            tail, IRFTitle, description, affected, IRFNo, ROED, potROEDs = readIRF(file, CN)
            if ROED:
                # data = IRFdataForm(CN, tail, IRFTitle, description, affected, IRFNo, ROED, potROED, request.POST.get("dart"), request.POST.get("mod"), request.FILES.get('file').name)
                # print(data)
                # if data.is_valid():
                #     data.save()
                return render(request, 'MADI/ROED.html', {'potROEDs' : potROEDs, 'hook' : hook, 'punch' : punch})
            else:  
                writeERF(CN, tail, IRFTitle, description, affected, IRFNo, ROED, False, potROEDs, dart, mod, file.name)
        else:
            return render(request, 'MADI/home.html', {'form' : uploadForm, 'hook' : hook, 'punch' : punch, 'warning' : 'ERROR: Some fields were not filled out correctly. Please make sure your ERF path is valid.'})
    return redirect('HOME-home')

def createERF(request):
    writeERF(CN, tail, IRFTitle, description, affected, IRFNo, ROED, False, potROEDs, dart, mod, file.name)
    return redirect('HOME-home')