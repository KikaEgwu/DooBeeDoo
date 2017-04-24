from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from models import User, Poke
# Create your views here.
def index(request):
	return render(request, 'exam/index.html')

def register(request):
	did_register = User.objects.user_register(request)

	if did_register:
		return redirect(reverse('dashboard'))
	else:
		return redirect(reverse('index'))

def logon(request):
	did_login = User.objects.logon(request)

	if did_login:
		return redirect(reverse('dashboard'))
	else:
		return redirect(reverse('index'))

def logout(request):
	return render(request, 'exam/index.html')

def dashboard(request):

	users = User.objects.all()
	pokes = Poke.objects.all()

	count = 0

	for poke in pokes:
		if poke.pokedwho == request.session['logged_in_user']:
			count += 1

	context = {

		"users": users,
		"pokes": pokes,
		"count": count,
		}	
	return render(request, 'exam/dashboard.html', context)

def poke(request):
	did_poke = User.objects.poke(request)

	return redirect(reverse('dashboard'))