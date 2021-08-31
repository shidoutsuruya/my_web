from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
# Create your views here.
def index(request):
    """search for info"""
    ulist=User.objects.all()
    context={'userlist':ulist}
    return render(request,'myadmin/user/index.html',context)
def add(request):
    """add info"""
def insert(request):
    """insert info"""
def edit(request,uid=0):
    """edit info"""
def delete(request,uid=0):
    """delete info"""
def update(request,uid=0):
    """update info"""