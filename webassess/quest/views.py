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
            saveobj.save()
        for k in qmap.keys():
            print k,qmap[k]
            ansSave = -1
            for ans in saveobj.saves.all():
                if ans.question.id==int(k): ansSave=ans
            ansSave.choice = AnswerOption.objects.get(id=int(qmap[k]))
            ansSave.save()
        grade(saveobj)
        return redirect("/")

def grade(tsave):
    for ansSave in tsave.saves.all():
        try:
            if ansSave.choice.text == ansSave.question.answer.text:
                ansSave.correct=True
                ansSave.save()
        except: pass
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
        title = request.POST.get('testtitle')
        data = request.POST.get('data')
        enddate = int(request.POST.get('enddate'))
        jdat = json.loads(data)
        print json.dumps(jdat, sort_keys=True, indent=4, separators=(',', ':'))
        print title
        print enddate
        tobj = Test(
            name = title,
            creator=Teacher.objects.get(user=request.user),
            enddate=datetime.datetime.now() + datetime.timedelta(days=enddate)
        )
        tobj.save()
        for q in jdat:
            ques = Question(
                    qtype = str(q[u'type']),
                    header = str(q[u'title']),
                    )
            ques.save()
            print "so far"
            for opt in q[u'options']:
                aopt = AnswerOption(text=opt[u'html'])
                print "so far far"
                aopt.save()
                ques.choices.add(aopt)
            if u'correct' in q:
                print "Correct answer",q[u'correct'][u'html']
                right = AnswerOption(text=q[u'correct'][u'html'])
                right.save()
                ques.answer = right
            else:
                print "[WARNING] No Correct Answer"
            ques.save()
            tobj.questions.add(ques)
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

@login_required
@user_passes_test(lambda u: len(Teacher.objects.filter(user=u)) > 0, login_url='/login/?req=teacher')
def del_view(request):
    if request.POST:
        id = request.POST.get('id')
        Test.objects.get(id=id).delete()
    return redirect("/")

