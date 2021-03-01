from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.core.paginator import Paginator

from core.models import OnlineOrder, Personnel, Customer, CustomerPhoneNo, PersonnelPhoneNo, Branch
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
                        full_price['total'] += order.food.price

                totals.append(full_price)

            ######

            personnel_as_customer_orders = OnlineOrder.objects.filter(
                deliverer=this_perssonel,
                delivery_status=OnlineOrder.IS_DELIVERING,
                customer=None
            )

            

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
                        full_price['total'] += order.food.price

                personnel_as_customer_totals.append(full_price)
            
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
                'personnels_delivery_destination_and_paycodes':personnels_delivery_destination_and_paycodes
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

