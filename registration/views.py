from django.shortcuts import get_object_or_404, render
from django.http import *
from django.urls import reverse
from django.template import loader, Context
from django.contrib.auth.models import User
from django.core.validators import *
from django.core.mail import *
from django.conf import settings
import hashlib
# Create your views here.

def register(request):
	if(request.method == "POST"):
		username  = request.POST.get("username")
		try:
			user = User.objects.get(username=username)
		except Exception as e:
			pass
		else:
			cont =  {'error':"There is a user with this username :/"}
			return render(request,  "registration/register.html", cont)

		
		email  = request.POST.get("email")
		try:
			validate_email(email)
		except Exception as e:
			cont =  {'error':"email is not valid :/"}
			return render(request,  "registration/register.html", cont)

		try:
			user = User.objects.get(email=email)
		except Exception as e:
			pass
		else:
			cont =  {'error':"There is a user with this email :/"}
			return render(request,  "registration/register.html", cont)

		pwd = request.POST.get("password")
		repwd = request.POST.get("repassword")
		if(pwd != repwd):
			cont =  {'error':"Passwords doesnt match :/"}
			return render(request,  "registration/register.html", cont)

		#new_user = User.objects.create_user(username, email, pwd)
		#new_user.save()

		u_id = User.objects.get(username = username).id
		active_link =  "http://" + request.META["HTTP_HOST"] + "/accounts/verify/" + u_id + "/" + hashlib.md5((username + email + "HELL").encode()).hexdigest() 
		send_mail('activitation link', 'activate your account and confirm your mail with this link: \n' + active_link, settings.EMAIL_HOST_USER ,[email], fail_silently=False)
		return HttpResponse("new user created and verify email sent, now just go and login :))")

			
			
	cont =  {'error':"sign up here!!"}
	return render(request,  "registration/register.html", cont)
