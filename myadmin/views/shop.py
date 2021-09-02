#views for shop
from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
from django.core.paginator import Paginator
import hashlib
from datetime import datetime
import random
from myadmin.models import Shop
import os
# Create your views here. 

def index(request,pIndex=1,item_per_page=10):
    """search for info"""
    slist=Shop.objects.all().exclude(status=3)
    mywhere=[]#to keep status of filter
    #get keyword from html form
    keyword=request.GET.get('keyword',None)
    if keyword!=None:
        slist=slist.filter(name__contains=keyword)
        mywhere.append('keyword='+keyword)
    #page seperate
    status=request.GET.get('status','')
    if status!='':
        slist=slist.filter(status=status)
        mywhere.append('status='+status)
    slist=slist.order_by('id')#get now page
    pIndex=int(pIndex)
    page=Paginator(slist,item_per_page)
    maxpages=page.num_pages
    if pIndex>maxpages:
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)#get this page
    plist=page.page_range
    items_count=page.count
    for i in list2:
        print(i.cover_pic)
    context={'shoplist':list2,'maxpages':maxpages,'plist':plist,\
             'items_count':items_count,'pIndex':pIndex,\
             'keyword':keyword,'mywhere':mywhere}
    return render(request,'myadmin/shop/index.html',context)
def add(request):
    """add info"""
    return render(request,"myadmin/shop/add.html")
def insert(request):
    """insert info"""
    try:
        #picture load
        myfile=request.FILES.get('img',None)
        if not myfile:
            return HttpResponse('no picture info')
        cover_pic=datetime.now().strftime("%Y%m%d-%h%M%d")+'.'+myfile.name.split('.').pop()
        img_path=os.path.join('static','upload','shop','img',cover_pic)
        print('image path:',img_path)
        with open(img_path,'wb+') as f:
            for chunk in myfile.chunks():
                f.write(chunk)
        print('picture load')
        #logo load 
        myfile=request.FILES.get('logo',None)
        if not myfile:
            return HttpResponse('no logo info')
        banner_pic=datetime.now().strftime("%Y%m%d-%h%M%d")+'.'+myfile.name.split('.').pop()
        logo_path=os.path.join('static','upload','shop','logo',banner_pic)
        print('logo path:',logo_path)
        with open(logo_path,'wb+') as f:
            for chunk in myfile.chunks():
                f.write(chunk)
        print('logo load')
        #text load
        obj=Shop()
        obj.name=request.POST['name']
        obj.address=request.POST['address']
        obj.phone=request.POST['phone']
        obj.status=1
        obj.cover_pic=cover_pic
        obj.banner_pic=banner_pic
        obj.create_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        obj.save()
        context={'info':'insert successfully'}       
    except Exception as err:
        print(err)
        context={"info":'insert failed'}
    return render(request,'myadmin/info.html',context)
    

def edit(request,sid=0):
    """edit info"""
    try:
        obj=Shop.objects.get(id=sid)
        context={'shop':obj}
        return render(request,'myadmin/shop/edit.html',context)
    except Exception as err:
        print(err)
        context={"info":'not find infomation need to be edited'}
        return render(request,'myadmin/info.html',context)
def delete(request,sid=0):
    try:
        obj=Shop.objects.get(id=sid)
        obj.status=3 
        obj.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.save()
        context={"info":'suceessful'}
    except Exception as err:
        print(err)
        context={"info":'fail to delete'}
    print(context)
    return render(request,'myadmin/info.html',context)
def update(request,sid=0):
    """update info"""
    try:
        obj=Shop.objects.get(id=sid)
        obj.status=request.POST['status']
        obj.name=request.POST['name']
        obj.address=request.POST['address']
        obj.phone=request.POST['phone']
        obj.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.save()
        context={'info':'successfully update'}
    except  Exception as err:
        print(err)
        context={"info":'update failed'}
    return render(request,'myadmin/info.html',context)
        
