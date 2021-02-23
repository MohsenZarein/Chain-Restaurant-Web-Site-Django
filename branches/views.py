from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST

from core.models import Branch

class BranchView(View):

    @method_decorator(require_GET)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

    def get(self, request, branch_code):
        branch = get_object_or_404(Branch, branch_code=branch_code)
        context = {
            'branch':branch
        }
        return render(request, 'branches/branch.html', context)
        