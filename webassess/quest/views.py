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
import time
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
    
def add_view(request):
    return render(request, 'quest/add.html', {})

def add_submit(request):
    if request.POST:
        data = request.POST.get('data')
        enddate = request.POST.get('enddate')
        jdat = json.loads(data)
        print jdat,"loaded"
        tobj = Test(
            creator=Teacher.objects.get(user=request.user),
            enddate=time.strptime(str(enddate), '%m/%d/%Y %H:%M')
        )
        tobj.save()
        for opt in jdat.options:
            aopt = AnswerOption(html=opt.html)
            tobj.questions.add(aopt)
        tobj.save()
        
        
    return HttpResponse("")
