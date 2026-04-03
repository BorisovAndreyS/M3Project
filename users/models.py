from django.contrib.auth.models import AbstractUser
from django.db import models
from validaters.validaters import validate_phone

# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # objects = models.Manager()

    email = models.EmailField(unique=True)

    phone = models.CharField(unique=True, max_length=20, null=True, blank=True, validators=[validate_phone])

    image = models.ImageField(upload_to='profile_images',
                              default='profile_images/default.png',
                              null=True, blank=True
                              )
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['email']

    def __str__(self):
        return self.email
