#cart info
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
def add(request,pid):
    get_product=request.session['productlist'][pid]
    # add buy product num
    get_product['num']=1
    # try getting cart info from session
    cartlist=request.session.get('cartlist',{})
    # judge whether the dish is in cart
    if pid in cartlist:
        cartlist[pid]['num']+=1
    else:
        cartlist[pid]=get_product
    request.session['cartlist']=cartlist
    return redirect(reverse('web_index'))
def delete(request,pid):
    cartlist=request.session.get('cartlist',{})
    del cartlist[pid]
    #put new cartlist into session
    request.session['cartlist']=cartlist
    return redirect(reverse('web_index'))
def clear(request):
    request.session['cartlist']={}
    return redirect(reverse('web_index'))
def change(request):
    print('cahgngeee')
    cartlist=request.session.get('cartlist',{})
    #get the dish id need to be changed
    pid=request.GET.get('pid',0)
    m=int(request.GET.get('num',1))
    if m<1:
        m=1
    cartlist[pid]['num']=m
     #put new cartlist into session
    request.session['cartlist']=cartlist
    return redirect(reverse('web_index'))
        