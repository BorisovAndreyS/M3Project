from django.views.generic import CreateView, FormView

from users.forms import UserRegistrationForm, UserLoginForm


class UserCreationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = '/'


# class UserLoginView(CreateView):
#     form_class = UserLoginForm
#     template_name = 'login.html'
#     success_url = '/'
