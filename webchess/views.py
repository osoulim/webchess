from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.http import HttpResponse
from .models import *

@login_required
def index(request):
    return HttpResponse("fuck the system")