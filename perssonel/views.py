from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from core.models import OnlineOrder, Personnel, Customer, CustomerPhoneNo, Branch
from uuid import uuid4



class PerssonelDashboardView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    
    def get(self, request):
        
        user = request.user

        if user.is_staff:
            
            this_perssonel = user.personnel
            orders = OnlineOrder.objects.filter(
                deliverer=this_perssonel,
                delivery_status=OnlineOrder.IS_DELIVERING
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
            
            context = {
                'orders':orders,
                'totals':totals,
                'customers':customers_to_be_serviced,
                'customers_to_be_serviced_phone_no':customers_to_be_serviced_phone_no,
                'customers_delivery_destination_and_paycodes':customers_delivery_destination_and_paycodes 
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

            customer = Customer.objects.get(
                customer_id=request.POST['customer_id']
            )
            personnel = request.user.personnel

            orders = OnlineOrder.objects.filter(
                customer=customer,
                deliverer=personnel
            )

            for order in orders:
                order.delivery_status = OnlineOrder.DELIVERED
                order.save()

            messages.success(request, 'انجام شد')
            return redirect('perssonel-dashboard')
        
        else:

            return HttpResponseForbidden()


