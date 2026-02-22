from django.shortcuts import render
from django.views.generic import CreateView

from users.forms import UserCreationForm


# Create your views here.

class UserCreationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
