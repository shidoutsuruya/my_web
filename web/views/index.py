from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
import urllib
import json
# Create your views here.
def index(request):
    #main idex
    return redirect(reverse('web_index'))
def web_index(request):
    return render(request,"web/index.html")
def login(request):
    """join in login"""
    return render(request,'web/login.html')
def dologin(request):
    
         #recaptcha
        recaptcha_response=request.POST.get('g-recaptcha-response')
        verify_url='https://www.recaptcha.net/recaptcha/api/siteverify'
        values={
            'secret':settings.RECAPTCHA_PRIVATE_KEY,
            'response':recaptcha_response
        }
        data=urllib.parse.urlencode(values).encode()
        req=urllib.request.Request(verify_url,data=data)
        response=urllib.request.urlopen(req)
        result=json.loads(response.read().decode())
def logout(request):
    pass
def verify(request):
    pass
