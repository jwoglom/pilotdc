from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from quest.models import Test
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
            {'questions': test.questions.all() }
            )
