from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
from django.core.paginator import Paginator
import hashlib
from datetime import datetime
import random
# Create your views here. 
def index(request,pIndex=1,item_per_page=10):
    """search for info"""
    ulist=User.objects.all().exclude(status=3)
    mywhere=[]#to keep status of filter
    #get keyword from html form
    keyword=request.GET.get('keyword',None)
    if keyword!=None:
        ulist=ulist.filter(username__contains=keyword)
        mywhere.append('keyword='+keyword)
    #page seperate
    pIndex=int(pIndex)
    page=Paginator(ulist,item_per_page)
    maxpages=page.num_pages
    if pIndex>maxpages:
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)#get this page
    plist=page.page_range
    items_count=page.count
    context={'userlist':list2,'maxpages':maxpages,'plist':plist,
             'items_count':items_count,'pIndex':pIndex,
             'keyword':keyword,'mywhere':mywhere}
    return render(request,'myadmin/user/index.html',context)
def add(request):
    """add info"""
    
    return render(request,"myadmin/user/add.html")
def insert(request):
    """insert info"""
    hash=hashlib.md5()
    try:
        obj=User()
        obj.username=request.POST['username']
        if request.POST['re_password']!=request.POST['password']:
            context={'info':'twice password input is not same'}
            return render(request,'myadmin/info.html',context)
        obj.password_salt=str(random.randint(100000,999999))
        string=request.POST['password']+obj.password_salt
        hash.update(string.encode('utf-8'))#md5
        obj.password_hash=hash.hexdigest()
        obj.status=1
        obj.create_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.save()
        context={"info":'suceessful'}
    except Exception as err:
        print(err)
        context={"info":'fail'}
    print(context)
    return render(request,'myadmin/info.html',context)

def edit(request,uid=0):
    """edit info"""
    try:
        obj=User.objects.get(id=uid)
        context={'user':obj}
        return render(request,'myadmin/user/edit.html',context)
    except Exception as err:
        print(err)
        context={"info":'not find infomation need to be edited'}
        return render(request,'myadmin/info.html',context)
def delete(request,uid=0):
    try:
        obj=User()
        obj=User.objects.get(id=uid)
        obj.status=3 
        obj.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.save()
        context={"info":'suceessful'}
    except Exception as err:
        print(err)
        context={"info":'fail'}
    print(context)
    return render(request,'myadmin/info.html',context)
def update(request,uid=0):
    """update info"""
    try:
        obj=User.objects.get(id=uid)
        obj.status=request.POST['status']
        obj.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.save()
        context={'info':'successfully update'}
    except  Exception as err:
        print(err)
        context={"info":'update failed'}
    return render(request,'myadmin/info.html',context)
        