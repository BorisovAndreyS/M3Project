from django.contrib import messages
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
from django.urls import reverse, reverse_lazy
from users.forms import UserRegistrationForm, UserLoginForm, ProfileForm
from django.contrib.auth import login, logout

from users.models import User


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



class AccountView(TemplateView):
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.request.user.user_order.all()
        return context

class ProfileFormView(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'account.html'
    success_url = reverse_lazy('users:account')


    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        request = self.request
        messages.success(request, f'Профиль обновлен!')
        return response









