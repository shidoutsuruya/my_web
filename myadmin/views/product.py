from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
from myadmin.models import Category,Shop,Product
import time,os
def index(request,pIndex=1,per_page=10):
    ulist=Product.objects.filter(status=1)
    mywhere=[]
    kw=request.GET.get("keyword",None)
    if kw:
        ulist=ulist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
    status=request.GET.get("status",'')
    #category search
    cid=request.GET.get("category_id",None)
    if cid:
        ulist=ulist.filter(category_id=cid)
        mywhere.append('category_id='+cid)
    status=request.GET.get("status",'')
    if status!="":
        ulist=ulist.filter(status=status)
        mywhere.append('status='+status)
    ulist=ulist.order_by('id')
    #page
    pIndex=int(pIndex)
    page=Paginator(ulist,per_page)
    maxpages=page.num_pages
    if pIndex>maxpages:
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)
    plist=page.page_range
    #traversal product info to shop info
    for prod in list2:
        shop_obj=Shop.objects.get(id=prod.shop_id)
        prod.shopname=shop_obj.name
        cate_obj=Category.objects.get(id=prod.category_id)
        prod.category_name=cate_obj.name
    
    context={"productlist":list2,'plist':plist,
             'pIndex':pIndex,'maxpages':maxpages,'keyword':kw}
    return render(request,'myadmin/product/index.html',context)
def add(request):
    #get allshop info
    slist=Shop.objects.values('id','name')
    context={"shoplist":slist}
    return render(request,'myadmin/product/add.html',context)
def insert(request):
    try:
        #picture get
        myfile=request.FILES.get("cover_pic",None)
        if not myfile:
            return HttpResponse('NO INFO')
        cover_pic=str(time.time())+'.'+myfile.name.split('.').pop()
        with open(os.path.join("./static/upload/product",cover_pic,'wb+')) as f:
            for chunk in myfile.chunks():
                f.write(chunk)
        #get insert object
        obj=product()
        obj.shop_id=request.POST['shop_id']
        obj.category_id=request.POST['category_id']
        obj.name=request.POST['name']
        obj.price=request.POST['price']
        obj.cover_pic=cover_pic
        obj.status=1 
        obj.create_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.save() 
        context={"info":'insert successfully'}
    except Exception as err:
        print('error:',err)
        context={'info':'insert failed'}
    return render(request,'myadmin/info.html',context)
def delete(request,pid=0):
    try:
        obj=product.objects.get(id=pid)
        obj.status=0
        obj.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.save()
        context={'info':'delete successfully'}
    except Exception as err:
        print(err)
        context={'info':'delete failed'}
    return render(request,'myadmin/info.html',context)
def edit(request,pid=0):
    try:
        obj=product.objects.get(id=pid)
        context={'product':obj}
        slist=Shop.objects.values('id','name')
        context["shoplist"]=slist
        print(context)
        return render(request,'myadmin/product/edit.html',context) 
    except Exception as err:
        print(err)
        context={'info':'not find data need to be edited'}
        return render(request,'myadmin/info.html',context)
def update(request,pid=0):
    try:
        obj=product.objects.get(id=pid)
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