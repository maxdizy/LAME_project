import os
import random
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .MADI_config import readIRF, writeERF
from MADI.forms import uploadForm
from .models import config
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from LAME.settings import get_file

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
        if form.is_valid():
            form.save()
        global CN, tail, IRFTitle, description, affected, IRFNo, ROED, potROEDs, dart, mod, file, URL
        CN, file, dart, mod = request.POST.get('caseNo'), request.FILES.get('file'), request.POST.get("dart"), request.POST.get("mod")
        tail, IRFTitle, description, affected, IRFNo, ROED, potROEDs, URL = readIRF(file, CN)
        if ROED:
            return render(request, 'MADI/ROED.html', {'potROEDs' : potROEDs, 'hook' : hook, 'punch' : punch})
        else:  
            writeERF(CN, tail, IRFTitle, description, affected, IRFNo, ROED, False, potROEDs, dart, mod, URL)
    return redirect('HOME-home')

@login_required
def createERF(request):
    writeERF(CN, tail, IRFTitle, description, affected, IRFNo, ROED, False, potROEDs, dart, mod, URL)
    with open(URL, 'rb') as erf:
        content = erf.read()
    # Set the return value of the HttpResponse
    response = HttpResponse(content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = 'attachment; filename= "{}"'.format(CN + "-" + tail + "-" + IRFTitle + ".docx")
    # Return the response value
    os.remove(URL)
    return response