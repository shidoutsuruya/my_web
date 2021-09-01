from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
import hashlib
from datetime import datetime
import random
from django.shortcuts import redirect
from django.urls import reverse
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
        obj=User.objects.exclude(status=3).get(username=request.POST['username'])
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
    except Exception as err:
        print(err)
        context={'info':"login failed"}
    return render(request,'myadmin/index/login.html',context)
def logout(request):
    print('request_session is :',request.session)
    print('request_session adminuser :',request.session['adminuser'])
    del request.session['adminuser']
    return redirect(reverse('myadmin_login'))