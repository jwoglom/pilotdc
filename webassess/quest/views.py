from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from quest.models import AnswerOption, Question, Test
#, AnswersSave, AnswerSave
import json
from quest.models import Test
from django.utils import timezone
@login_required
def take_view(request, test_id):
    try:
        test_id = int(test_id)
    except:
        return render(request, 'quest/expired.html')
    test = -1
    for x in Test.objects.order_by('id'):
        print x.id
        if x.id == test_id:
            test=x
    if test==-1:# or test.enddate < timezone.now():
        return render(request, 'quest/expired.html')
    return render(request, 'quest/take.html', {})

"""
@login_required
def submit_view(request):
    def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
    def json2obj(data): return json.loads(data, object_hook=_json_object_hook)'

    if request.POST:
        testid = request.POST.get('testid')
        mapstr = request.POST.get('map')
        questionstr = request.POST.get('questions')
        map = json2obj(mapstr)
        questions = json2obj(questionstr)

        testobj = Test.objects.get(id=testid)
        save = AnswersSave(
            test=testobj
        )
        save.save()
        save.saves.add(
            test=testobj,
            saves=
        )
"""
