from django.shortcuts import  get_object_or_404, redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core import exceptions

from core.models import Branch, Food, OnlineOrder


class OrderView(View):

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    
    def get(self, request, branch_code):

        branch = get_object_or_404(Branch, branch_code=branch_code)
        foods = Food.objects.all()
        context = {
            'foods':foods,
            'branch':branch
        }
        return render(request, 'order/order.html', context)

    
    def post(self, request, branch_code):

        branch = get_object_or_404(Branch, branch_code=branch_code)
        food_id = int(request.POST['food_id'])
        food = Food.objects.get(pk=food_id)
        count = int(request.POST['count'])

        if request.user.is_staff:
            
            personnel_as_customer = request.user.personnel
            
            try:
                order = OnlineOrder.objects.get(
                    personnel_as_customer=personnel_as_customer,
                    branch=branch,
                    food=food,
                    delivery_status=OnlineOrder.NOT_DELIVERED
                )
                order.count = order.count + count
                print(order.count)
                order.save()
                foods = Food.objects.all()
                context = {
                    'foods':foods,
                    'branch':branch
                }
                messages.success(request, "به سبد سفارش های شما اضافه شد , برای ثبت نهایی به داشبورد خود مراجعه کنید")
                return render(request, 'order/order.html', context)
                
            except exceptions.ObjectDoesNotExist:
                OnlineOrder.objects.create(
                    personnel_as_customer=personnel_as_customer,
                    customer=None,
                    branch=branch,
                    food=food,
                    count=count
                ).save()
                foods = Food.objects.all()
                context = {
                    'foods':foods,
                    'branch':branch
                }
                messages.success(request, 'به سبد سفارش های شما اضافه شد , برای ثبت نهایی به داشبورد خود مراجعه کنید')
                return render(request, 'order/order.html', context)
        
        else:

            customer = request.user.customer
            
            try:
                order = OnlineOrder.objects.get(
                    customer=customer,
                    branch=branch,
                    food=food,
                    delivery_status=OnlineOrder.NOT_DELIVERED
                )
                order.count = order.count + count
                print(order.count)
                order.save()
                foods = Food.objects.all()
                context = {
                    'foods':foods,
                    'branch':branch
                }
                messages.success(request, "به سبد سفارش های شما اضافه شد , برای ثبت نهایی به داشبورد خود مراجعه کنید")
                return render(request, 'order/order.html', context)
                
            except exceptions.ObjectDoesNotExist:
                OnlineOrder.objects.create(
                    customer=customer,
                    personnel_as_customer=None,
                    branch=branch,
                    food=food,
                    count=count
                ).save()
                foods = Food.objects.all()
                context = {
                    'foods':foods,
                    'branch':branch
                }
                messages.success(request, 'به سبد سفارش های شما اضافه شد , برای ثبت نهایی به داشبورد خود مراجعه کنید')
                return render(request, 'order/order.html', context)

        

        



