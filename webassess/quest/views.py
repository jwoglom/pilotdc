from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect
from quest.models import TestSave, AnswerOption, Question, Test, AnswerSave
#, AnswersSave, AnswerSave
import json
from quest.models import Test
from users.models import Teacher
from django.utils import timezone
from IPython import embed
import json
import datetime
import pytz

@login_required
@user_passes_test(lambda u: len(Teacher.objects.filter(user=u)) > 0, login_url='/login/?req=teacher')
def teacher_view(request):
    test_list = Test.objects.order_by('-postdate')
    return render(request, 'quest/teacher.html', {'tests': test_list})


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

@login_required
def submit_view(request):
#    def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
#    def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
    if request.POST:
        testid = request.POST.get('testid')
        mapstr = request.POST.get('map')
        questionstr = request.POST.get('questions')
        sender = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
        print sender,type(sender)
        print sender.student
        sender = sender.student
        qmap = json.loads(mapstr)
        print qmap,"was loaded"
        #questions = json2obj(questionstr) #Afaik I know this is pointless
        testobj = Test.objects.get(id=testid)

        try:
            print "Trying..."
            print sender.testsave_set
            print type(testobj)
            saveobj = sender.testsave_set.get(test=testobj)
            print "TestSave already exists"
        except:
            print "Must create new test"
            saveobj = TestSave(
                    user = sender,
                    test=testobj
            )
            saveobj.save()
        print "Prepped the saveobj"
        for testq in testobj.questions.all():
            print testq
            new=AnswerSave(question = testq, correct = False)
            new.save()
            saveobj.saves.add(new)
            print "Added"
        for k in qmap.keys():
            ansSave = saveobj.saves.get(id=int(k))
            ansSave.choice = AnswerOption.objects.get(id=int(qmap[k]))
            ansSave.save()
        grade(saveobj)
        return redirect("/")

def grade(tsave):
    for ansSave in tsave.saves.all():
        if ansSave.choice == ansSave.question.answer:
            ansSave.correct=True
            ansSave.save()
    for ansSave in tsave.saves.all():
        if ansSave.correct: 
            tsave.score+=1
            tsave.save()

@login_required
@user_passes_test(lambda u: len(Teacher.objects.filter(user=u)) > 0, login_url='/login/?req=teacher')
def add_view(request):
    return render(request, 'quest/add.html', {})

@login_required
@user_passes_test(lambda u: len(Teacher.objects.filter(user=u)) > 0, login_url='/login/?req=teacher')
def add_submit(request):
    if request.POST:
        data = request.POST.get('data')
        enddate = int(request.POST.get('enddate'))
        jdat = json.loads(data)
        print enddate
        tobj = Test(
            creator=Teacher.objects.get(user=request.user),
            enddate=datetime.date.today() + datetime.timedelta(days=enddate)
        )
        tobj.save()
        for opt in jdat[u'options']:
            aopt = AnswerOption(text=opt[u'html'])
            tobj.questions.add(aopt)
        tobj.save()
        
        
    return HttpResponse("")

@login_required
@user_passes_test(lambda u: len(Teacher.objects.filter(user=u)) > 0, login_url='/login/?req=teacher')
def edit_view(request, test_id):
    try:
        test_id = int(test_id)
    except:
        return render(request, 'quest/expired.html')
    test = -1
    try: 
        test = Test.objects.get(id=test_id)
    except: 
        return render(request, 'quest/expired.html')
    if test==-1:
        return render(request, 'quest/expired.html')
    return render(request, 'quest/edit.html', {
        'questions': test.questions.all(),
        'testid': test_id,
        'testtitle': test.name,

    })
