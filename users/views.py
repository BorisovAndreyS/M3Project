from django.views.generic import CreateView

from users.forms import UserRegistrationForm


class UserCreationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = '/'
