from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OrderForm(forms.Form):
    deliveryAddress = forms.CharField(max_length=128, label='Delivery address')


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, label='First name', required=True)
    last_name = forms.CharField(max_length=150, label='Last name', required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class FeedbackForm(forms.Form):
    feedback_text = forms.CharField(label='Leave feedback', max_length=512,
                                    widget=forms.Textarea(attrs={'rows': '5', 'style':'resize:none'}))
