from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone 

from quest.models import Test
import datetime

@login_required
def dashboard_view(request):
    test_list = Test.objects.order_by('-postdate')
    for x in test_list:
        print x.postdate,timezone.now()
    before = [x for x in test_list if x.enddate < timezone.now()]
    after = [x for x in test_list if x not in before]
    ids = [x.test.id for x in request.user.student.testsave_set.all()]
    return render(request, 'dashboard.html', {'before': before, 'after': after,
        'ids': ids })
