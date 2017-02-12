from django.shortcuts import get_object_or_404, render
from django.http import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *


@login_required
def index(request):
    return render(request, "webchess/game.html")

