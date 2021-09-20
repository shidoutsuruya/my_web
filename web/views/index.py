from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
import urllib
import json
import hashlib
from web.models import *
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
        if result['success']==False:
            return redirect(reverse('web_login')+"?errinfo=2")
        #user identification
        user=User.objects.get(username=request.POST['username'])
        if user.status==6 or user.status==1:
            md5=hashlib.md5() 
            s=request.POST['pass']+user.password_salt
            md5.update(s.encode('utf-8'))
            if user.password_hash==md5.hexdigest():
                print('successfully login')
                request.session['webuser']=user.to_dict()
                return redirect(reverse("web_index"))
            else:
                return redirect(reverse('web_login')+'?errinfo=5')
        else:
            return redirect(reverse('web_login')+'?errinfo=4')
    
        #print(err)
        #return redirect(reverse('web_login')+'?errinfo=3')
        
            
def logout(request):
    pass
