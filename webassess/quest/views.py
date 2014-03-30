from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from quest.models import TestSave, AnswerOption, Question, Test
#, AnswersSave, AnswerSave
import json
from quest.models import Test
from users.models import Teacher
from django.utils import timezone

@login_required
def take_view(request, test_id):
    try:
        test_id = int(test_id)
    except:
        return render(request, 'quest/expired.html')
    test = -1
    try: 
        test = Test.objects.get(id=test_id)
    except: 
        return render(request, 'quest/expired.html')
    if test==-1 or test.enddate < timezone.now():
        return render(request, 'quest/expired.html')
    #print test.questions.all()
    return render(request, 
            'quest/take.html', 
            {'questions': test.questions.all(), 'testid': test_id }
            )
    return render(request, 'quest/take.html', {})

@login_required
def submit_view(request):
#    def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
#    def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
    if request.POST:
        testid = request.POST.get('testid')
        mapstr = request.POST.get('map')
        questionstr = request.POST.get('questions')
        qmap = json.loads(mapstr)
        print qmap
        questions = json2obj(questionstr) #Afaik I know this is pointless

        testobj = Test.objects.get(id=testid)
        save = TestSave(
            test=testobj
        )
        save.save()
        #save.saves.add(
        #    test=testobj,
        #    saves=
        #)

@user_passes_test(lambda u: len(Teacher.objects.filter(user=u)) > 0, login_url='/login/?req=teacher')
def add_view(request):
    return render(request, 'quest/add.html', {})

@user_passes_test(lambda u: len(Teacher.objects.filter(user=u)) > 0, login_url='/login/?req=teacher')
def add_submit(request):
    pass