from django.contrib.auth.forms import UserCreationForm, forms

from users.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'example@gmail.com', 'class': 'Input'}),
            'username': forms.TextInput(attrs={'placeholder': 'Your username', 'class': 'Input'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'Input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Your last name', 'class': 'Input'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'qwerty123', 'class': 'Input'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'qwerty123', 'class': 'Input'}),
        }
        labels = {
            'email': 'Email',
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is alread in use')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'palceholder': 'example@gmail.com', 'class': 'Input'}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'qwerty123', 'class': 'Input'}))

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        self.fields['username'].label = 'Email'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'city', 'address', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'Input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Your last name', 'class': 'Input'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your phone', 'class': 'Input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@gmail.com', 'class': 'Input'}),
            'city': forms.TextInput(attrs={'placeholder': 'Your city', 'class': 'Input'}),
            'address': forms.TextInput(attrs={'placeholder': 'Your address', 'class': 'Input'}),
        }
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'phone': 'Phone',
            'email': 'Email',
            'city': 'City',
            'address': 'Address',
            'image': 'Image',
        }
