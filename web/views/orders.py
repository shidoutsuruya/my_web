from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from myadmin.models import User,Orders,OrderDetail,Payment
from django.core.paginator import Paginator 
def index(request,pIndex=1):
    umod=Orders.objects
    sid=request.session['shopinfo']['id']
    ulist=umod.filter(shop_id=sid)
    mywhere=[]
    status=request.GET.get('status','')
    if status=='':
        ulist=ulist.filter(status=status)
        mywhere.append('status='+status)
    ulist=ulist.order_by('id')
    pIndex=int(pIndex)
    page=Paginator(ulist,10)
    maxpages=page.num_pages
    if pIndex>maxpages:
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)
    plist=page.page_range
    context={'orderslist':list2,'plist':plist,
             'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    for vo in list2:
        if vo.user_id==0:
            vo.nickname='null'
        else:
            user=User.objects.only('nickname').get(id=vo.user_id)
            vo.nickname=user.nickname
    return render(request,'web/list.html',context)
def insert(request):
    try:
        ord=Orders()
        ord.shop_id=request.session['shopinfo']['id']
        ord.member_id=0
        ord.user_id=request.session['webuser']['id']
        ord.money=request.session['total']
        ord.status=1
        ord.payment_status=2
        ord.create_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ord.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ord.save()
        #payinfo add
        pay=Payment()
        pay.order_id=ord.id
        pay.member_id=0
        pay.type=2
        pay.bank=request.GET.get('bank',3)
        pay.money=request.session['total']
        pay.status=2      
        pay.create_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pay.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pay.save()
        #order detail
        cartlist=request.session.get('cartlist',{})
        for cart in cartlist.values():
            od=OrderDetail()
            od.order_id=od.id
            od.product_id=cart['id']
            od.product_name=cart['name']
            od.price=cart['price']
            od.quantity=cart['num']
            od.status=1
            od.save()
        #clear cartlist
        del request.session['cartlist']
        del request.session['total']
        return HttpResponse('yes')
    except Exception as err:
        print(err)
        return HttpResponse('no')
def detail(request):
    pass
def status(request):
    pass