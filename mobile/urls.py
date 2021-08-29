from mobile.views import index
from django.urls import path

urlpatterns = [
    path('', index.index,name='mobile_index'),
]
