from django import forms
from .models import ProductComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }