from myadmin.views import index
from django.urls import path

urlpatterns = [
    path('', index.index,name='myadmin_index'),
]
