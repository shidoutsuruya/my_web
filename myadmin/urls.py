from myadmin.views import index,user,shop
from django.urls import path
urlpatterns = [
    path('', index.index,name='myadmin_index'),
    #login url
    path('login',index.login,name="myadmin_login"),
    path('dologin',index.dologin,name="myadmin_dologin"),
    path('logout',index.logout,name="myadmin_logout"),
    #admin url
    path('user/<int:pIndex>',user.index,name='myadmin_user_index'),
    path('user/add',user.add,name='myadmin_user_add'),
    path('user/insert',user.insert,name='myadmin_user_insert'),
    path('user/del/<int:uid>',user.delete,name="myadmin_user_delete"),
    path('user/edit/<int:uid>',user.edit,name='myadmin_user_edit'),
    path('user/update/<int:uid>',user.update,name='myadmin_user_update'),
    #shop url
    path('shop/<int:pIndex>',shop.index,name='myadmin_shop_index'),
    path('shop/add',shop.add,name='myadmin_shop_add'),
    path('shop/insert',shop.insert,name='myadmin_shop_insert'),
    path('shop/del/<int:sid>',shop.delete,name="myadmin_shop_delete"),
    path('shop/edit/<int:sid>',shop.edit,name='myadmin_shop_edit'),
    path('shop/update/<int:sid>',shop.update,name='myadmin_shop_update'),
]

handler404=index.page_not_found
