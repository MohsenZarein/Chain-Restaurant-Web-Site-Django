from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages

from core.models import Branch

class IndexView(View):

    @method_decorator(require_GET)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        branches = Branch.objects.all()
        context = {
            'branches':branches
        }
        
        return render(request, 'pages/index.html',context)


class LoginView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

    def get(self, request):
        return render(request, 'pages/login.html')
    

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(
            email=email,
            password=password
            )
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                #return redirect('manager-dashboard')
                return HttpResponse(status=200)
            elif user.is_staff:
                #return redirect('personnel-dashboard')
                return HttpResponse(status=200)
            else:
                return redirect('customer-dashboard')            
        else:
            messages.error(request, "ایمیل یا پسورد اشتباه است")
            return redirect('login')




class LogoutView(View):

    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        logout(request)
        messages.success(request, 'از حساب خود خارج شدید')
        return redirect('index')




        


        
    

