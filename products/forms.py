from django import forms

from products.models import Review


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'detail']
        widgets = {
            'rating': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Your comment',
                'class': 'Input'}),
            'detail': forms.Textarea(attrs={
                'class': 'Input',
                'rows': 5,
                'placeholder': 'Your text',
            }),
        }

        labels = {
            'rating': 'Rating',
            'comment': 'Comment',
            'detail': 'Detail',
        }
