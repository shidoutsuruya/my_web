from django.shortcuts import redirect
from django.urls import reverse
import re
class Middleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        path=request.path
        url_list=['/myadmin/login','/myadmin/logout','/myadmin/dologin']
        #judge if match myadmin exclude url_list
        if re.match(r'^/myadmin',path) and (path not in url_list):
            #use session
            if 'adminuser' not in request.session:
                
                return redirect(reverse("myadmin_login"))
        #judge if match web exclude url_list
        if re.match(r'^/web',path):
            #use session
            if 'webuser' not in request.session:
                return redirect(reverse("web_login")) 
        #end   
        response=self.get_response(request)
        return response