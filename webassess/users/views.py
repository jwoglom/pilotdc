from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.sites.models import Site, get_current_site
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import RequestContext, loader
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def process_login(request):
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)

		if user is not None and user.is_active:
			login(request, user)
			next_page = request.POST.get('next', None)
			if next_page is not None:
				return redirect(next_page)
			else:
				return redirect('/')
	
	next_page = request.GET.get('next', None)
		
	context = {
		'next': next_page,
	}
	return render(request, 'login.html', context)

def process_logout(request):
	logout(request)
	return redirect("/")

def http403(request):
	template = loader.get_template('resources/http403.html')
	return HttpResponseForbidden(template.render(RequestContext(request)))

@login_required
def admin_index(request):
	user = request.user
	
	if not user.groups.filter(name="admins").exists():
		raise

	school = user.staff.school

	context = {
		'user': user,
		'school': school,
		'view': 'admin_index',
		'is-admin': True,
	}

	if staticfiles_storage.exists("css/{}.css".format(school.number)):
		context['school_theme'] = "css/{}.css".format(school.number)

	return render(request, 'resources/admin_index.html', context)
