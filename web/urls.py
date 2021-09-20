from web.views import index
from django.urls import path,include
urlpatterns = [
    path('', index.index,name='index'),
    path('login',index.login,name='web_login'),
    path('dologin',index.dologin,name='web_dologin'),
    path('logout',index.logout,name='web_logout'),
    #request login
    path('web/',include([
        path('', index.web_index,name='web_index'),
    ]))
]