from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.UserCreationView.as_view(), name='register' ),
]

