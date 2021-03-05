from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.core import exceptions

from core.models import (OnlineOrder, Order, Personnel, Customer,
                         CustomerPhoneNo, PersonnelPhoneNo, Branch, Food,
                         Table, Store, StoreBranch)
                          
from uuid import uuid4
from datetime import datetime




class PerssonelDashboardView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    
    def get(self, request):
        
        user = request.user

    
        if user.is_staff and not user.is_superuser:
            
            this_perssonel = user.personnel

            orders = OnlineOrder.objects.filter(
                deliverer=this_perssonel,
                delivery_status=OnlineOrder.IS_DELIVERING,
                personnel_as_customer=None
            )
            if orders:

                all_customers = Customer.objects.all()
                customers_to_be_deleted = []

                for customer in all_customers:

                    if not orders.filter(customer=customer).exists():
                        customers_to_be_deleted.append(customer.customer_id)
                
                customers_to_be_serviced = Customer.objects.exclude(
                    customer_id__in=customers_to_be_deleted
                )

                customers_to_be_serviced_phone_no = CustomerPhoneNo.objects.filter(
                    customer__in=customers_to_be_serviced
                )

                customers_delivery_destination_and_paycodes = []
                
                for customer in customers_to_be_serviced:
                    for order in orders:
                        if order.customer.customer_id == customer.customer_id:
                            res = {
                                'customer_id':customer.customer_id,
                                'destination':order.destination_address,
                                'pay_code':order.pay_code
                            }
                            customers_delivery_destination_and_paycodes.append(res)
                            break
                
                totals = []

                for customer in customers_to_be_serviced:
                    full_price = {
                        'customer_id':customer.customer_id,
                        'total':0
                    }
                    for order in orders:
                        if order.customer.customer_id == customer.customer_id:
                            full_price['total'] += order.food.price * order.count

                    totals.append(full_price)

            else:

                customers_to_be_serviced = None
                customers_to_be_serviced_phone_no = None
                customers_delivery_destination_and_paycodes = None
                totals = None

            ##########

            personnel_as_customer_orders = OnlineOrder.objects.filter(
                deliverer=this_perssonel,
                delivery_status=OnlineOrder.IS_DELIVERING,
                customer=None
            )

            if personnel_as_customer_orders:

                all_personnels = Personnel.objects.all().exclude(personnel_code=this_perssonel.personnel_code)
                personnels_to_be_deleted = []

                for personnel in all_personnels:

                    if not personnel_as_customer_orders.filter(personnel_as_customer=personnel).exists():
                        personnels_to_be_deleted.append(personnel.personnel_code)
                
                personnels_to_be_serviced = Personnel.objects.exclude(
                    personnel_code__in=personnels_to_be_deleted
                ).exclude(personnel_code=this_perssonel.personnel_code)

                personnels_to_be_serviced_phone_no = PersonnelPhoneNo.objects.filter(
                    personnel__in=personnels_to_be_serviced
                )

                personnels_delivery_destination_and_paycodes = []
                
                for personnel in personnels_to_be_serviced:
                    for order in personnel_as_customer_orders:
                        if order.personnel_as_customer.personnel_code == personnel.personnel_code:
                            res = {
                                'personnel_code':personnel.personnel_code,
                                'destination':order.destination_address,
                                'pay_code':order.pay_code
                            }
                            personnels_delivery_destination_and_paycodes.append(res)
                            break
                
                personnel_as_customer_totals = []

                for personnel in personnels_to_be_serviced:
                    full_price = {
                        'personnel_code':personnel.personnel_code,
                        'total':0
                    }
                    for order in personnel_as_customer_orders:
                        if order.personnel_as_customer.personnel_code == personnel.personnel_code:
                            full_price['total'] += order.food.price * order.count

                    personnel_as_customer_totals.append(full_price)

            else:
                
                personnels_to_be_serviced = None
                personnels_to_be_serviced_phone_no = None
                personnels_delivery_destination_and_paycodes = None
                personnel_as_customer_totals = None

            ############

            orders_registered_by_manager = Order.objects.filter(
                servant=this_perssonel,
                delivery_status=Order.NOT_DELIVERED
            )
            print(orders_registered_by_manager)
            if orders_registered_by_manager:

                all_tables = Table.objects.filter(branch=request.user.personnel.branch)
                tables_to_be_deleted = []

                for table in all_tables:

                    if not orders_registered_by_manager.filter(table=table).exists():
                        tables_to_be_deleted.append(table.pk)
                
                tables_to_be_serviced = Table.objects.filter(
                    branch=request.user.personnel.branch
                ).exclude(
                    pk__in=tables_to_be_deleted
                )

                tables_totals = []

                for table in tables_to_be_serviced:
                    full_price = {
                        'table_id':table.pk,
                        'total':0
                    }
                    for order in orders_registered_by_manager:
                    
                        if order.table.pk == table.pk:
                            full_price['total'] += order.food.price * order.count

                    tables_totals.append(full_price)
            else:

                tables_to_be_serviced = None
                tables_totals = None


            context = {
                'orders':orders,
                'totals':totals,
                'customers':customers_to_be_serviced,
                'customers_to_be_serviced_phone_no':customers_to_be_serviced_phone_no,
                'customers_delivery_destination_and_paycodes':customers_delivery_destination_and_paycodes,
                'personnel_as_customer_orders':personnel_as_customer_orders,
                'personnel_as_customer_totals':personnel_as_customer_totals,
                'personnels':personnels_to_be_serviced,
                'personnels_to_be_serviced_phone_no':personnels_to_be_serviced_phone_no,
                'personnels_delivery_destination_and_paycodes':personnels_delivery_destination_and_paycodes,
                'orders_registered_by_manager':orders_registered_by_manager,
                'tables_to_be_serviced':tables_to_be_serviced,
                'tables_totals':tables_totals
            }

            return render(request, 'perssonel/perssonel-dashborad.html', context)

        else:

            return HttpResponseForbidden()


class PersonneDashboardSelfOrdersView(View):

    @method_decorator(login_required)
    @method_decorator(require_GET)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)
    

    def get(self, request):

        if request.user.is_staff:

            orders = OnlineOrder.objects.filter(
                personnel_as_customer=request.user.personnel
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

        

            context = {
                'orders':orders,
                'branches_in_not_delivered_status':branches_in_not_delivered_status,
                'branches_in_is_delivering_status':branches_in_is_delivering_status,
                'branches_in_delivered_status':branches_in_delivered_status
            }

            return render(request, 'perssonel/personnel-dashboard-self-orders.html', context)

        else:
            
            return HttpResponseForbidden()



class FinalDeliveryView(View):

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def post(self, request):

        if request.user.is_staff:
            
            if request.POST.get('customer_id', default=None):

                customer = Customer.objects.get(
                    customer_id=request.POST['customer_id']
                )
                personnel = request.user.personnel

                orders = OnlineOrder.objects.filter(
                    customer=customer,
                    personnel_as_customer=None,
                    deliverer=personnel
                )

                for order in orders:
                    order.delivery_status = OnlineOrder.DELIVERED
                    order.save()

                messages.success(request, 'انجام شد')
                return redirect('perssonel-dashboard')
            
            elif request.POST.get('personnel_code', default=None):
                
                personnel_as_customer = Personnel.objects.get(
                    personnel_code=request.POST['personnel_code']
                )
                personnel = request.user.personnel

                orders = OnlineOrder.objects.filter(
                    customer=None,
                    personnel_as_customer=personnel_as_customer,
                    deliverer=personnel
                )

                for order in orders:
                    order.delivery_status = OnlineOrder.DELIVERED
                    order.save()
                
                messages.success(request, 'انجام شد')
                return redirect('perssonel-dashboard')
            
            elif request.POST.get('table_id', default=None):
                
                table = Table.objects.get(pk=int(request.POST['table_id']))
                servant = request.user.personnel

                orders = Order.objects.filter(
                    servant=servant,
                    table=table
                )

                for order in orders:
                    order.delivery_status = Order.DELIVERED
                    order.save()
                
                messages.success(request, 'انجام شد')
                return redirect('perssonel-dashboard')


            else:

                return HttpResponseBadRequest()

        
        else:

            return HttpResponseForbidden()




class RegisterAllPersonnelOrders(View):

    @method_decorator(login_required)
    @method_decorator(require_POST)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def post(self, request):
        
        if request.user.is_staff:

            personnel_as_customer = request.user.personnel
            destination = request.POST['destination']
            branch_code = request.POST['branch_code']

            branch = Branch.objects.get(branch_code=branch_code)

            not_delivered_orders = OnlineOrder.objects.filter(
                personnel_as_customer=personnel_as_customer,
                branch=branch,
                delivery_status=OnlineOrder.NOT_DELIVERED
            )

            if not not_delivered_orders:

                messages.error(request, 'سبد خرید شما خالی است')
                return redirect('personnel-dashboard-self-orders')

            else:

                pay_code = str(uuid4())
                
                personnels = Personnel.objects.filter(branch=branch)
                manager = None
                for p in personnels:
                    if p.user.is_superuser:
                        manager = p
                        break

                perssonel = Personnel.objects.filter(
                    branch=branch
                ).exclude(personnel_code=personnel_as_customer.personnel_code).exclude(
                    personnel_code=manager.personnel_code
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
                return redirect('personnel-dashboard-self-orders')
        
        else:

            return HttpResponseForbidden()



class PersonnelInfoView(View):

    @method_decorator(login_required)
    @method_decorator(require_GET)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    
    def get(self, request):

        if request.user.is_superuser:

            personnels = Personnel.objects.filter(
                branch=request.user.personnel.branch
            ).exclude(personnel_code=request.user.personnel.personnel_code)

            paginator = Paginator(personnels,3)
            page_number = request.GET.get('page')
            paged_personnels = paginator.get_page(page_number)

            context = {
                'personnels':paged_personnels
            }

            return render(request, 'perssonel/personnel-info.html', context)

        else:

            return HttpResponseForbidden()



class AddPersonnelView(View):

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)
    

    def get(self, request):

        if request.user.is_superuser:

            personnels = Personnel.objects.filter(branch=request.user.personnel.branch)

            context = {
                'personnels':personnels
            }

            return render(request, 'perssonel/add-personnel.html', context)

        else:

            return HttpResponseForbidden()
    

    def post(self, request):

        if request.user.is_superuser:

            email = request.POST.get('email')
            if not get_user_model().objects.filter(email=email).exists():

                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')

                if password1 == password2:

                    first_name = request.POST.get('first_name')
                    last_name = request.POST.get('last_name')
                    gender = request.POST.get('gender')
                    birth_date = request.POST.get('birth_date')
                    salary = request.POST.get('salary')
                    province = request.POST.get('province')
                    city = request.POST.get('city')
                    street = request.POST.get('street')
                    alley = request.POST.get('alley')
                    supervisor_code = request.POST.get('supervisor')

                    if gender == 'M':
                        gender = 'مرد'
                    else:
                        gender = 'زن'

                    user = get_user_model().objects.create_user(
                        email=email,
                        password=password1
                    )
                    user.is_staff = True
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()

                    if supervisor_code == "None":

                        Personnel.objects.create(
                            user=user,
                            province=province,
                            city=city,
                            street=street,
                            alley=alley,
                            gender=gender,
                            personnel_code=int(str(uuid4().fields[-1])),
                            birth_date=birth_date,
                            salary=salary,
                            branch=request.user.personnel.branch
                        )

                    else:

                        supervisor = Personnel.objects.get(personnel_code=int(supervisor_code))

                        Personnel.objects.create(
                            user=user,
                            province=province,
                            city=city,
                            street=street,
                            alley=alley,
                            gender=gender,
                            personnel_code=int(str(uuid4().fields[-1])),
                            birth_date=birth_date,
                            salary=salary,
                            branch=request.user.personnel.branch,
                            supervisor=supervisor,
                        )


                    messages.success(request, 'پرسنل مورد نظر ثبت شد')
                    return redirect('add-personnel')
                
                else:

                    messages.error(request, 'پسورد ها مشابه نیستند')
                    return redirect('add-personnel')

            else:

                messages.error(request, 'این ایمیل قبلا در سیستم ثبت شده')
                return redirect('add-personnel')
            
        else:

            return HttpResponseForbidden()



class DeletePersonnelView(View):

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)
    

    def get(self, request):

        if request.user.is_superuser:

            personnels = Personnel.objects.filter(
                branch=request.user.personnel.branch
                ).exclude(personnel_code=request.user.personnel.personnel_code)

            context = {
                'personnels':personnels
            }

            return render(request, 'perssonel/delete-personnel.html', context)

        else:

            return HttpResponseForbidden()


    def post(self, request):

        if request.user.is_superuser:

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            personnel_code = request.POST.get('personnel_code')

            try:
                
                personnel = Personnel.objects.get(personnel_code=int(personnel_code))
                user = personnel.user

                if personnel.branch.branch_code == request.user.personnel.branch.branch_code:

                    if user.first_name == first_name and user.last_name == last_name:

                        user.delete()
                        messages.success(request, 'پرسنل مورد نظر از سیستم حذف شد')
                        return redirect('delete-personnel')
                    
                    else:

                        messages.error(request, 'نام و نام خانوادگی با کد پرسنلی مطابقت ندارد')
                        return redirect('delete-personnel')
                else:

                    messages.error(request, ' هیچ پرسنلی با این کد در این شعبه ثبت نشده است')
                    return redirect('delete-personnel')

            except exceptions.ObjectDoesNotExist:

                messages.error(request, 'هیچ پرسنلی با این کد پرسنلی در سیستم ثبت نشده است')
                return redirect('delete-personnel')



class RegisterOrderByManager(View):

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    
    def get(self, request):

        if request.user.is_superuser:

            foods = Food.objects.all()

            tables = Table.objects.filter(
                branch=request.user.personnel.branch,
                is_empty=True
                )

            personnels = Personnel.objects.filter(
                branch=request.user.personnel.branch
                ).exclude(personnel_code=request.user.personnel.personnel_code)

            context = {
                'foods':foods,
                'personnels':personnels,
                'tables':tables
            }

            return render(request, 'perssonel/register-order-by-manager.html', context)
        
        else:

            return HttpResponseForbidden()
    

    def post(self, request):


        if request.user.is_superuser:

            food = Food.objects.get(pk=int(request.POST.get('food')))
            personnel = Personnel.objects.get(personnel_code=int(request.POST.get('personnel')))
            count = int(request.POST.get('count'))
            table_id = request.POST.get('table')

            table = Table.objects.get(pk=int(table_id))
            Order.objects.create(
                branch=request.user.personnel.branch,
                table=table,
                food=food,
                servant=personnel,
                pay_code=str(uuid4()),
                count=count
            )
            
            messages.success(request, 'ثبت شد')
            return redirect('register-order-by-manager')
        
        else:

            return HttpResponseForbidden()



class StoreView(View):

    @method_decorator(login_required)
    @method_decorator(require_GET)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)
    

    def get(self, request):

        if request.user.is_staff:

            store_branch = StoreBranch.objects.filter(branch=request.user.personnel.branch)
            store_code = []
            for i in store_branch:
                store_code.append(i.store.store_code)

            store_product = Store.objects.filter(store_code__in=store_code)
            print(store_product)

            

            context = {
                'store_branch':store_branch,
                'store_product':store_product
            }
            print(store_branch)
            print(store_product)
            return render(request, 'perssonel/stores.html', context)

        else:

            return HttpResponseForbidden()
            





            
                




