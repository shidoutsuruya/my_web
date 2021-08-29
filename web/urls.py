from web.views import index
from django.urls import path
urlpatterns = [
    path('', index.index,name='web_index'),
]