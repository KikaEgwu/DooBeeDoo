from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
from datetime import datetime
from dateutil.parser import parse as parse_date
# Create your models here.
class UserManager(models.Manager):
	def user_register(self, request):
		is_valid = True

		if len(request.POST['name']) == 0:
			messages.error(request, 'Name is Required')
			is_valid = False

		if len(request.POST['alias']) == 0:
			messages.error(request, 'Alias is Required')
			is_valid = False

		email_match = User.objects.filter(email=request.POST['email'])

		if len(email_match) > 0:
			messages.error(request, "This email is already in use")
			is_valid = False

		if len(request.POST['password']) < 8:
			messages.error(request, 'Password needs to be at least 8 characters long')
			is_valid = False

		if request.POST['password'] != request.POST['confirm_password']:
			messages.error(request, "The passwords don't match")
			is_valid = False

		if not is_valid:
			return False

		hashed = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())

		new_user = User(
			name = request.POST['name'],
			alias = request.POST['alias'],
			email = request.POST['email'],
			pwhash = hashed,
			dateofbirth = request.POST['dateofbirth'],
			pokes = 0,
			)
		new_user.save()
		request.session['logged_in_user'] = new_user.id
		request.session['username'] = new_user.name
		return True

	def logon(self, request):
		users = User.objects.filter(email=request.POST['email'])

		if len(users) == 0:
			messages.error(request, "User does not exist")
			return False

		user = users[0]

		hashedpw = bcrypt.hashpw(request.POST['password'].encode('utf-8'), user.pwhash.encode('utf-8'))

		if hashedpw != user.pwhash:
			messages.error(request, 'Password is incorrect')
			return False

		request.session['logged_in_user'] = user.id
		request.session['username'] = user.name
		return True

	def logout(self, request):
		request.session['logged_in_user'] = null
		request.session['username'] = null

	def poke(self, request):
		gettingpoked = User.objects.get(id=request.POST['poke'])

		gettingpoked.pokes += 1

		gettingpoked.save()

		poking = User.objects.get(id=request.session['logged_in_user'])

		test1 = Poke.objects.filter(user=poking).filter(pokedwho=gettingpoked.id)
		
		if len(test1) > 0:
			test = test1[0]
			test.pokes += 1
			test.save()
		else:
			poker = Poke(
				pokes = 1,
				user = poking,
				pokedwho = gettingpoked.id,
				)
			poker.save()

class User(models.Model):
	name = models.CharField(max_length=100)
	alias = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	pwhash = models.CharField(max_length=150)
	pokes = models.IntegerField()
	dateofbirth = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = UserManager()

class Poke(models.Model):
	pokes = models.IntegerField()
	user = models.ForeignKey(User)
	pokedwho = models.IntegerField()

	objects = UserManager()