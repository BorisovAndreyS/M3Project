from django.contrib import messages
from django.views.generic import CreateView, FormView, TemplateView
from django.urls import reverse
from users.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, logout


class UserCreationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        messages.success(self.request, f'Добро пожаловать, {user.username}!')
        return response

    def get_success_url(self):

        return reverse('products:products_list')


# class UserLoginView(CreateView):
#     form_class = UserLoginForm
#     template_name = 'login.html'
#     success_url = '/'


class AccountView(TemplateView):
    template_name = 'account.html'




