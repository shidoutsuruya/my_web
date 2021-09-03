from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
from myadmin.models import Category,Shop

def index(request,pIndex=1,per_page=10):
    ulist=Category.objects.filter(status__lt=9)
    mywhere=[]
    kw=request.GET.get("keyword",None)
    if kw:
        ulist=ulist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
    status=request.GET.get("status",'')
    if status!="":
        ulist=ulist.filter(status=status)
        mywhere.append('status='+status)
    ulist=ulist.order_by('id')
    pIndex=int(pIndex)
    page=Paginator(ulist,per_page)
    maxpages=page.num_pages
    if pIndex>maxpages:
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)
    plist=page.page_range
    #traversal category info to shop info
    for cate in list2:
        shop_obj=Shop.objects.get(id=cate.shop_id)
        cate.shopname=shop_obj.name
    
    context={"categorylist":list2,'plist':plist,
             'pIndex':pIndex,'maxpages':maxpages,'keyword':kw}
    return render(request,'myadmin/category/index.html',context)
def add(request):
    #get allshop info
    slist=Shop.objects.values('id','name')
    context={"shoplist":slist}
    return render(request,'myadmin/category/add.html',context)
def insert(request):
    try:
        obj=Category()
        obj.shop_id=request.POST['shop_id']
        obj.name=request.POST['name']
        obj.status=1 
        obj.create_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.save() 
        context={"info":'insert successfully'}
    except Exception as err:
        print(err)
        context={'info':'insert failed'}
    return render(request,'myadmin/info.html',context)
def delete(request,cid=0):
    try:
        obj=Category.objects.get(id=cid)
        obj.staus=0
        obj.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.save()
        context={'info':'delete successfully'}
    except Exception as err:
        print(err)
        context={'info':'delete failed'}
    return render(request,'myadmin/info.html',context)
def edit(request,cid=0):
    try:
        obj=Category.objects.get(id=cid)
        context={'category':obj}
        slist=Shop.objects.values('id','name')
        context["shoplist"]=slist
        print(context)
        return render(request,'myadmin/category/edit.html',context) 
    except Exception as err:
        print(err)
        context={'info':'not find data need to be edited'}
        return render(request,'myadmin/info.html',context)
def update(request,cid=0):
    try:
        obj=Category.objects.get(id=cid)
        obj.shop_id=request.POST['shop_id']
        obj.name=request.POST['name']
        obj.status=request.POST['status']
        obj.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.save()
        context={'info':'successfully changed'}
    except Exception as err:
        print(err)
        context={'info':'changed failed'}
    return render(request,'myadmin/info.html',context)