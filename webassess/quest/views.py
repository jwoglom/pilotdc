from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from quest.models import Test
@login_required
def take_view(request, number):
    return render(request, 'quest/take.html', {})
