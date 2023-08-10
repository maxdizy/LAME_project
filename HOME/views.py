import random
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from HOME.forms import contactAdminForm
from LAME.settings import get_file

from pathlib import Path
import os
import psycopg2
import boto3
import json
import pickle
from django.core.files.storage import default_storage

joke = random.choice(get_file('data/jokes.txt').read().decode().splitlines())
joke = joke.split('<>')
hook = joke[0]
punch = joke[1]

def home(request):
    return render(request, 'HOME/home.html', {'hook' : hook, 'punch' : punch})

def planes(request):
    return render(request, 'HOME/planes.html', {'hook' : hook, 'punch' : punch})

def contactAdminPage(request):
    return render(request, 'HOME/contactAdmin.html', {'form' : contactAdminForm, 'warning' : '', 'success' : '', 'hook' : hook, 'punch' : punch})

def contactAdmin(request):
    import os
    from email.message import EmailMessage
    import ssl
    import smtplib

    # try:
    email_sender = 'lame.communication@gmail.com'
    email_pass = os.environ['EMAIL_PASS']
    email_reviever = 'maxwell.l.dizy@lmco.com'
    subject = 'LAME request - ' + request.POST.get('ID') + ' - ' + request.POST.get('request') + ' - ' + request.POST.get('email')
    body = request.POST.get('body')

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reviever
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=120) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email_sender, email_pass)
        server.sendmail(email_sender, email_reviever, em.as_string())
        server.quit()
    # except Exception as error:
    #     print(error)
    #     return render(request, 'HOME/contactAdmin.html', {'form' : contactAdminForm, 'warning' : 'error sending form.', 'success' : '', 'hook' : hook, 'punch' : punch})
    return render(request, 'HOME/contactAdmin.html', {'form' : contactAdminForm, 'warning' : '', 'success' : 'form sent successfully, you will recieve an email when approved.', 'hook' : hook, 'punch' : punch})

@login_required
def profile(request):
    return render(request, 'HOME/profile.html', {'hook' : hook, 'punch' : punch})

@login_required
def user_guide(request):
    userGuide = get_file('data/LAME User Guide.pdf').read()
    # Set the return value of the HttpResponse
    UserGuideresponse = HttpResponse(userGuide, content_type='application/pdf')
    # Set the HTTP header for sending to browser
    UserGuideresponse['Content-Disposition'] = 'attachment; filename= "LAME User Guide.pdf"'
    # Return the response value
    return UserGuideresponse
