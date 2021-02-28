from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseBadRequest

from core.models import Table, ReserveTable, Branch
from datetime import datetime



class ReservationView(View):

    @method_decorator(login_required)
    @method_decorator(require_GET)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)
    

    def get(self, request, branch_code):
        
        branch = get_object_or_404(Branch, branch_code=branch_code)
        context = {
            'branch':branch
        }
        return render(request, 'reservation/reservation.html', context)
    


class ReserveTableView(View):

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)


    def post(self, request):

        branch = get_object_or_404(Branch, branch_code=request.POST.get('branch_code'))
        count = int(request.POST.get('count'))
        date = request.POST.get('date')

        if date < str(datetime.now().date()):

            messages.error(request, 'تاریخ رزرو  نامعتبر است')
            return redirect('/reservation/'+str(branch.branch_code))

        
        reservations = ReserveTable.objects.filter(
            branch=branch,
        )
        
        reserved_tables = []
        for reserve in reservations:
            if str(reserve.date) == date:
                reserved_tables.append(reserve.table.pk)
        
        tables = Table.objects.filter(branch=branch).exclude(pk__in=reserved_tables)
        

        if tables:

            table = None
            for t in tables:
                if t.capacity >= count:
                    table = t
                    break
            
            if table:
                
                if request.user.is_staff:
                    
                    ReserveTable.objects.create(
                        branch=branch,
                        personnel_as_customer=request.user.personnel,
                        customer=None,
                        date=date,
                        table=table
                    )

                else:
                    
                    ReserveTable.objects.create(
                        branch=branch,
                        personnel_as_customer=None,
                        customer=request.user.customer,
                        date=date,
                        table=table
                    )



                messages.success(request, 'میز شماره {0} برای شما رزرو شد'.format(table.pk))
                return redirect('/reservation/'+str(branch.branch_code))

            else:

                messages.error(request, 'میزی متناسب با ظرفیت درخواستی شماموجود نیست')
                return redirect('/reservation/'+str(branch.branch_code))

        else:

            messages.error(request, 'در حال حاضر هیج میز خالی ای در این تاریخ و شعبه وجود ندارد')
            return redirect('/reservation/'+str(branch.branch_code))

    