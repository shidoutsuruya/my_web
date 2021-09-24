from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
import urllib
import json
import hashlib
from myadmin.models import User,Shop,Category,Product
# Create your views here.
def index(request):
    #main idex
    return redirect(reverse('web_index'))
def web_index(request):
    #get cartlist from session to sum up price
    cartlist=request.session.get('cartlist',{})
    total=0
    #statistic price
    for dish in cartlist.values():
        total+=dish['num']*dish['price']
    request.session['total']=total
    context={'categorylist':request.session.get('categorylist',{}).items()}
    return render(request,"web/index.html",context)
def login(request):
    #option shows
    shoplist=Shop.objects.filter(status=1)
    context={'shoplist':shoplist}
    return render(request,'web/login.html',context)
def dologin(request):       
    try:
        #select shop
        if request.POST['shop_id']=='0':
            return redirect(reverse('web_login')+'?errinfo=1')       
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
                #get shop info
                shopobj=Shop.objects.get(id=request.POST['shop_id'])
                request.session['shopinfo']=shopobj.to_dict()
                #get all category
                clist=Category.objects.filter(shop_id=shopobj.id,status=1)
                categorylist=dict()
                productlist=dict()
                #traverse category info
                for user in clist:
                    c={'id':user.id,'name':user.name,'pids':[]}
                    plist=Product.objects.filter(category_id=user.id,status=1)
                    #tranverse dish info in present category
                    for p in plist:
                        c['pids'].append(p.to_dict())
                        productlist[p.id]=p.to_dict()
                    categorylist[user.id]=c
                #save info into session
                request.session['categorylist']=categorylist
                request.session['productlist']=productlist
                return redirect(reverse("web_index"))
            else:
                return redirect(reverse('web_login')+'?errinfo=5')
        else:
            return redirect(reverse('web_login')+'?errinfo=4')
    except Exception as err:
        print(err)
        return redirect(reverse('web_login')+'?errinfo=3')
        
            
def logout(request):
    del  request.session['webuser']
    return redirect(reverse('web_login'))
