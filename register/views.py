import random
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404



# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            form.save()
            #get the new user info
            user = User.objects.get(username=uname)
            user.save()
            return redirect('login')

        return redirect("index")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})



