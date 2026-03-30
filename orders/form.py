from django import forms

from validaters.validaters import validate_phone


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'Input'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'Input'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'Input'}), validators=[validate_phone] )
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'Input'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'Textarea', 'rows': 3}))
    payment_method = forms.ChoiceField(
        choices=[('debit', 'Debit Card'), ('wallet', 'Digital Wallet'), ('cod', 'Cash On Delivery')],
        widget=forms.RadioSelect
    )