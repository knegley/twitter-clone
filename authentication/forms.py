from django import forms


class LogInForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class Twitter_User_Signup(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(min_length=10, max_length=35)


class TweetForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, max_length=140)
