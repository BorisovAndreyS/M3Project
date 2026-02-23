from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = models.EmailField(unique=True)

    phone = models.CharField(unique=True, max_length=20, null=True, blank=True)

    image = models.ImageField(upload_to='profile_images',
                              default='profile_images/default.png',
                              null=True, blank=True
                              )



    def __str__(self):
        return self.email
