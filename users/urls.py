from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users import views
from .forms import UserLoginForm

app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreationView.as_view(), name='register' ),
    path('login/', LoginView.as_view(template_name='login.html',
                                     # authentication_form = UserLoginForm,
                                     redirect_authenticated_user=True,
                                     success_url='products:products_list',
                                     ), name='login'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('logout/', LogoutView.as_view(next_page = '/', )),
]

