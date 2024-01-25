from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50, label="Your name")
    email = forms.EmailField(label="Your email address")
    to = forms.EmailField(label="Recipient's email address")
    comments = forms.CharField(label="Add a message",
                               required=False,
                               widget=forms.Textarea(attrs={'rows': 5}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        labels = {'name': 'Your name', 'body': 'Comment'}


class SearchForm(forms.Form):
    query = forms.CharField(
        label=False,
    )
