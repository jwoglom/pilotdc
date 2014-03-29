from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def take_view(request):
    return render(request, 'quest/take.html', {})