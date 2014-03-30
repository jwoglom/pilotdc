from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.utils import timezone 

from users.models import Student, Teacher
from quest.models import Test
import datetime

@login_required
@user_passes_test(lambda u: len(Student.objects.filter(user=u)) > 0, login_url='/dashboard/teacher/')
def dashboard_view(request):
    test_list = Test.objects.order_by('-postdate')
    for x in test_list:
        print x.postdate,timezone.now()
    
    ids = [x.test for x in request.user.student.testsave_set.all()]
    tests=[]
    for x in test_list: 
        if x.enddate < timezone.now():
            time = "-1"
        else: time = "1"
        if x in ids: 
            score = request.user.student.testsave_set.get(id=x.id).score
            tests.append((x,time,score))
        else:
            tests.append((x,time,"-1"))

#    scores = []
#    for id in ids:
#        scores.append(id,request.user.student.testsave_set.get(id=id).score)
    print tests
    return render(request, 'dashboard.html', {'tests': tests})

@login_required
@user_passes_test(lambda u: len(Teacher.objects.filter(user=u)) > 0, login_url='/login/?req=teacher')
def teacher_view(request):
    test_list = Test.objects.order_by('-postdate')
    for x in test_list:
        print x.postdate,timezone.now()
    before = [x for x in test_list if x.enddate < timezone.now()]
    after = [x for x in test_list if x not in before]
    return render(request, 'teacher-dashboard.html', {'before': before, 'after': after})
