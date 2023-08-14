import os
import random
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .MADI_config import readIRF, writeERF, writeDart
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
        try:
            form = uploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            global CN, tail, IRFTitle, description, affected, IRFNo, ROED, potROEDs, dart, mod, IRFFile, URL
            CN, IRFFile, dart, mod = request.POST.get('caseNo'), request.FILES.get('IRFFile'), request.POST.get("dart"), request.POST.get("mod")
            tail, IRFTitle, description, affected, IRFNo, ROED, potROEDs, URL = readIRF(IRFFile, CN)
            if ROED:
                return render(request, 'MADI/ROED.html', {'potROEDs' : potROEDs, 'dart' : dart, 'hook' : hook, 'punch' : punch})
            else:  
                return redirect('MADI-createERF')
        except:
            return render(request, 'MADI/home.html', {'form' : uploadForm, 'hook' : hook, 'punch' : punch, 'warning' : 'form is not valid... you sure that\'s an IRF?'})
    return redirect('HOME-home')

@login_required
def createERF(request):
    ERFFile = request.FILES.get('ERFFile')
    writeERF(CN, tail, IRFTitle, description, affected, IRFNo, ROED, ERFFile, potROEDs, dart, mod, URL)
    with open(URL, 'rb') as erf:
        content = erf.read()
    # Set the return value of the HttpResponse
    response = HttpResponse(content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = 'attachment; filename= "{}"'.format(CN + "-" + tail + "-" + IRFTitle + ".docx")
    # Return the response value
    os.remove(URL)
    return response

def createDART(request):
    #dartPath = r'C:\Users\e443176\Documents\CLASSIFIED\case-tests\\' + 'DART-' + CN + '.pdf'
    dartPath = '/var/www/LAME_project/media/' + 'DART-' + CN + '.pdf'
    writeDart(tail, description, affected, dartPath, CN)
    with open(dartPath, 'rb') as dart:
        dartContent = dart.read()
    # Set the return value of the HttpResponse
    dartResponse = HttpResponse(dartContent, content_type='application/pdf')
    # Set the HTTP header for sending to browser
    dartResponse['Content-Disposition'] = 'attachment; filename= "{}"'.format("DART-" + CN + ".pdf")
    # Return the response value
    os.remove(dartPath)
    return dartResponse