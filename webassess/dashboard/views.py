from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from quest.models import Test
import datetime

@login_required
def dashboard_view(request):
    test_list = Test.objects.order_by('-postdate')
    before = [x for x in test_list if x.postdate < datetime.datetime.now]
    after = [x for x in test_list if x not in before]
    return render(request, 'dashboard.html', {'before': before, 'after': after})
