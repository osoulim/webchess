from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.http import *
from django.urls import reverse
from django.template import loader, Context
from django.contrib.auth.models import User
from django.core.validators import *
from django.core.mail import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import Game
import hashlib
from .ChessAI import *


def index(request):
	temp_cont = {'body' : "" , 'title' : "Welcome to the Chess game"}
	temp_cont['body'] = render_to_string("webchess/index.html")
	return render(request, "template.html", temp_cont)


@login_required
def game(request):
	if(not request.user.is_staff):
		HttpResponseRedirect(reverse("index"))
	temp_cont = {'body' : "" , 'title' : "The Game Page"}
	game = Game.objects.get(player = request.user)
	content = {"state" : game.state}
	temp_cont["body"] = render_to_string("webchess/game.html", content)
	return render(request, "template.html", temp_cont)

@login_required
def api(request):
	move = request.POST.get("move")
	move = move.split()
	move[0] = move[0][::-1]
	move = ' '.join(move)
	usr = request.user
	game = Game.objects.get(player = usr)
	tmp = chess(game.state)
	if(len(list(tmp.next_possible_moves(1))) == 0 and tmp.king_is_under_attack(1)):
		return HttpResponse("You LOST!!-" + game.state)
	if(len(list(tmp.next_possible_moves(1))) == 0 and (not tmp.king_is_under_attack(1))):
		return HttpResponse("POT-" + game.state)
	if(not tmp.user_move(move)):
		return HttpResponse("wrong way!-" + game.state)
	ai_move = alpha_beta_pruning(tmp, 4, a = -inf, b = inf, player = 0, maxim = 1)
	game.state = str(tmp)
	game.save()	
	if(ai_move[1] == None and tmp.king_is_under_attack(0)):
		return HttpResponse("AI Lost and YOU WON THE GAME!!-" + game.state)
	if(ai_move[1] == None and not tmp.king_is_under_attack(0)):
		return HttpResponse("POT-" + game.state)
	tmp.move(ai_move[1])
	game.state = str(tmp)
	game.save()

	return HttpResponse("ai move was:" + str(ai_move[1]) + "-" + game.state)

def login(request):
	temp_cont = {'body' : "" , 'title' : "login"}
	content = {"error" : ""}
	if(request.method == "GET"):
		temp_cont['body'] = render_to_string("registration/login.html", content)
		return render(request, "template.html", temp_cont)
	us = request.POST["username"]
	pwd = request.POST["password"]
	user = authenticate(username=us, password=pwd)
	if user is not None:
		auth_login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		content['error'] = "Username or Password in not correct"
		temp_cont['body'] =  render_to_string("registration/login.html", content)
		return render(request, "template.html", temp_cont)

def logout(request):
	auth_logout(request)
	return HttpResponseRedirect(reverse("index"))

   

def register(request):
	cont = {"error" : "Singup here!"}
	temp_cont = {'body' : "" , 'title' : "register"}

	if(request.method == "POST"):
		username  = request.POST.get("username")
		try:
			user = User.objects.get(username=username)
		except:
			pass
		else:
			cont['error']="There is a user with this username :/"
			temp_cont['body'] =  render_to_string("registration/register.html", cont)
			return render(request, "template.html", temp_cont)

		
		email  = request.POST.get("email")
		try:
			validate_email(email)
		except:
			cont['error']="email is not valid :/"
			temp_cont['body'] =  render_to_string("registration/register.html", cont)
			return render(request, "template.html", temp_cont)

		try:
			user = User.objects.get(email=email)
		except:
			pass
		else:
			cont['error']="There is a user with this email :/"
			temp_cont['body'] =  render_to_string("registration/register.html", cont)
			return render(request, "template.html", temp_cont)

		pwd = request.POST.get("password")
		repwd = request.POST.get("repassword")
		if(pwd != repwd):
			cont['error']="Passwords doesnt match :/"
			temp_cont['body'] =  render_to_string("registration/register.html", cont)
			return render(request, "template.html", temp_cont)


		new_user = User.objects.create_user(username, email, pwd)
		new_user.is_staff = False
		new_user.save()

		game = Game(player = new_user)
		game.save()

		u_id = new_user.id
		active_link =  "http://" + request.META["HTTP_HOST"] + "/verify/" + str(u_id) + "/" + hashlib.md5((username + email + "HELL").encode()).hexdigest() 
		send_mail('activitation link', 'activate your account and confirm your mail with this link: \n' + active_link, settings.EMAIL_HOST_USER ,[email], fail_silently=False)
		temp_cont['body'] = "new user created and verify email sent, now just go and login :))"
		return render(request, "template.html", temp_cont)
	
	temp_cont = {'body' : render_to_string("registration/register.html", cont) , 'title' : "register"}
	return render(request, "template.html", temp_cont)


def verify(request):
	temp_cont = {'body' : "" , 'title' : "Verify account"}
	u_id = request.path.split('/')[-2]
	u_hash = request.path.split('/')[-1]
	try:
		user = User.objects.get(id = u_id)
	except Exception as e:
		temp_cont['body'] = "this is a not a valid link :/"
		return render(request, "template.html", temp_cont)
	u_str = user.username + user.email + "HELL"
	if(hashlib.md5(u_str.encode()).hexdigest() != u_hash):
		temp_cont['body'] = "Hash code is not valid :/"
		return render(request, "template.html", temp_cont)

	user.is_staff = True
	user.save()
	temp_cont['body'] = "user activated :)"
	return render(request, "template.html", temp_cont);

@login_required
def reset_game(request):
	usr = request.user
	g = Game.objects.get(player = usr)
	g.reset_game()
	g.save()
	return HttpResponseRedirect(reverse("game"))