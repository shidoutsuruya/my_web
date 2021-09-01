from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
import hashlib
from datetime import datetime
import random
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
import urllib
import json
# Create your views here.
def page_not_found(request,exception=None):
    return render(request,'myadmin/index/404.html')
def index(request):
    return render(request,'myadmin/index/all-admin-index.html')
def login(request):
    return render(request,'myadmin/index/login.html')
def dologin(request):
    #check username and password
    hash=hashlib.md5()
    try:
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
        #check account password
        obj=User.objects.exclude(status=3).get(username=request.POST['username'])
        if result['success']==True:
            if obj.status==6:
                s=request.POST['pass']+obj.password_salt
                hash.update(s.encode('utf8'))
                if obj.password_hash==hash.hexdigest():
                #use session
                    request.session['adminuser']=obj.to_dict()
                    return redirect(reverse('myadmin_index'))
                else:
                    context={'info':"password wrong"}
            else:
                context={'info':"no admission"}
        else:
            context={'info':'please do recaptcha check'}
    except Exception as err:
        print(err)
        context={'info':"login failed"}
    return render(request,'myadmin/index/login.html',context)
def logout(request):
    print('request_session is :',request.session)
    print('request_session adminuser :',request.session['adminuser'])
    del request.session['adminuser']
    return redirect(reverse('myadmin_login'))