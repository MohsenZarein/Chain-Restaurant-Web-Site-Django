from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.core import exceptions

from core.models import Customer, CustomerPhoneNo, OnlineOrder, Branch, Personnel

from uuid import uuid4
from datetime import datetime


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
                    customer_id=int(str(uuid4().fields[-1])),
                )
                customer.save()

                CustomerPhoneNo.objects.create(
                    customer=customer,
                    phone=phone
                ).save()

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
    @method_decorator(require_GET)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)
    

    def get(self, request):

        if not request.user.is_staff:

            orders = OnlineOrder.objects.filter(
                customer=request.user.customer
            )

            branches = Branch.objects.all()

            branches_to_be_deleted_not_delivered = []
            branches_to_be_deleted_is_delivering = []
            branches_to_be_deleted_delivered = []
            
            for branch in branches:

                if not orders.filter(branch=branch, delivery_status=OnlineOrder.NOT_DELIVERED).exists():
                    branches_to_be_deleted_not_delivered.append(branch.branch_code)

                if not orders.filter(branch=branch, delivery_status=OnlineOrder.IS_DELIVERING).exists():
                    branches_to_be_deleted_is_delivering.append(branch.branch_code)
                    
                if not orders.filter(branch=branch, delivery_status=OnlineOrder.DELIVERED).exists():
                    branches_to_be_deleted_delivered.append(branch.branch_code)
                    
            branches_in_not_delivered_status = Branch.objects.exclude(
                branch_code__in=branches_to_be_deleted_not_delivered
                )
            branches_in_is_delivering_status = Branch.objects.exclude(
                branch_code__in=branches_to_be_deleted_is_delivering
                )
            branches_in_delivered_status = Branch.objects.exclude(
                branch_code__in=branches_to_be_deleted_delivered
                )

            phone_numbers = CustomerPhoneNo.objects.filter(customer=request.user.customer)

            context = {
                'orders':orders,
                'branches_in_not_delivered_status':branches_in_not_delivered_status,
                'branches_in_is_delivering_status':branches_in_is_delivering_status,
                'branches_in_delivered_status':branches_in_delivered_status,
                'phone_numbers':phone_numbers
            }

            return render(request, 'customer/dashboard.html', context)

        else:

            return HttpResponseBadRequest()

            

class RegisterAllOrdersView(View):

    @method_decorator(login_required)
    @method_decorator(require_POST)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)
    

    def post(self, request):

        customer = request.user.customer
        destination = request.POST['destination']
        branch_code = request.POST['branch_code']

        branch = Branch.objects.get(branch_code=branch_code)

        not_delivered_orders = OnlineOrder.objects.filter(
            customer=customer,
            branch=branch,
            delivery_status=OnlineOrder.NOT_DELIVERED
        )

        if not not_delivered_orders:

            messages.error(request, 'سبد خرید شما خالی است')
            return redirect('customer-dashboard')

        else:

            pay_code = str(uuid4())

            perssonel = Personnel.objects.filter(
                branch=branch
            ).order_by('last_service').first()
            perssonel.last_service = datetime.now()
            perssonel.save()

            for order in not_delivered_orders:
                order.delivery_status = OnlineOrder.IS_DELIVERING
                order.pay_code = pay_code
                order.destination_address = destination
                order.deliverer = perssonel
                order.save()
            
            messages.success(request, 'سفارش های های شما با موفقیت ثبت شد')
            return redirect('customer-dashboard')
        



class EditInfoView(View):

    @method_decorator(login_required)
    @method_decorator(require_POST)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)
    

    def post(self, request):

        if not request.user.is_staff:

            user = request.user
            customer = request.user.customer

            phone = request.POST.get('phone', default=None)
            if phone:
                if not CustomerPhoneNo.objects.filter(phone=phone,customer=customer).exists():
                    if not CustomerPhoneNo.objects.filter(customer=customer).count() >= 3 :
                        CustomerPhoneNo.objects.create(
                            phone=phone,
                            customer=customer
                        )
                    else:
                        messages.error(request, 'نمیتوانید بیشتر از سه شماره تماس ثبت کنید')
                        return redirect('customer-dashboard')
            
            first_name = request.POST.get('first_name', default=None)
            if first_name:
                user.first_name = first_name
                user.save()
             
            last_name = request.POST.get('last_name', default=None)
            if last_name:
                user.last_name = last_name
                user.save()
            
            province = request.POST.get('province', default=None)
            if province:
                customer.province = province
                customer.save()
            
            city = request.POST.get('city', default=None)
            if city:
                customer.city = city
                customer.save()
            
            street = request.POST.get('street', default=None)
            if street:
                customer.street = street
                customer.save()
            
            alley = request.POST.get('alley', default=None)
            if alley:
                customer.alley = alley
                customer.save()
            
            gender = request.POST.get('gender', default=None)
            if gender:
                if gender == "M":
                    customer.gender = "مرد"
                    customer.save()
                else:
                    customer.gender = "زن"
                    customer.save()
            
            messages.success(request, '! اطلاعات با موفقیت ویرایش شد ')
            return redirect('customer-dashboard')

        else:

            return HttpResponseBadRequest()



class DeleteOrderFromBasketView(View):

    @method_decorator(login_required)
    @method_decorator(require_POST)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)
    

    def post(self, request):
        
        try:

            OnlineOrder.objects.get(id=request.POST.get('order_id')).delete()
            messages.success(request, 'انجام شد')
            return redirect('customer-dashboard')

        except exceptions.ObjectDoesNotExist:

            messages.error(request, ' خطا! حذف از سبد انجام نشد')
            return redirect('customer-dashboard')

