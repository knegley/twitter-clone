from django import forms


class TweetForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, max_length=140)
