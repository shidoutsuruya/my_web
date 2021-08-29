from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    string='welcome order system,please order your dish.'
    return HttpResponse(string)