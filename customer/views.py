from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from core.models import Customer

from uuid import uuid4



class RegisterCustomerView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    
    def get(self, request):
        return render(request, 'customer/register.html')

    def post(self, request):
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        

        if password1 == password2 :

            if not get_user_model().objects.filter(email=email).exists():

                user = get_user_model().objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1
                )
                user.save()
                customer = Customer.objects.create(
                    user=user,
                    customer_id=int(str(uuid4().fields[-1])[:8]),
                )
                customer.save()
                messages.success(request, "ثبت نام با موفقیت انجام شد")
                return redirect('login')
                
            else:
                messages.error(request, "این ایمیل قبلا ثبت شده است")
                return redirect('customer-register')

        else:
            messages.error(request, "پسورد ها یکسان نیستند")
            return redirect('customer-register')



class DashboardView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

    def get(self, request):
        return render(request, 'customer/dashboard.html')

