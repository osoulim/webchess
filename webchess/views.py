from django.shortcuts import get_object_or_404, render
from django.http import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .ChessAI import *

@login_required
def index(request):
    return render(request, "webchess/game.html")

@login_required
def api(request):
	move = request.POST.get("move")
	usr = request.user
	game = Game.objects.get(player = usr)
	tmp = chess(game.state)
	if(not tmp.user_move(move)):
		return HttpResponse("")









	return HttpResponse()

