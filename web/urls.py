from web.views import index,cart,orders
from django.urls import path,include
urlpatterns = [
    path('', index.index,name='index'),
    path('login',index.login,name='web_login'),
    path('dologin',index.dologin,name='web_dologin'),
    path('logout',index.logout,name='web_logout'),
    #request login
    path('web/',include([
        path('', index.web_index,name='web_index'),
        path('cart/add/<str:pid>',cart.add,name='web_cart_add'),
        path('cart/delete/<str:pid>',cart.delete,name='web_cart_delete'),
        path('cart/clear',cart.clear,name='web_cart_clear'),
        path('cart/change',cart.change,name='web_cart_change'),
        #order handle
        path('orders/insert',orders.insert,name='web_orders_insert')
    ]))
]