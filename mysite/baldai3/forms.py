from django import forms
from .models import Profile, Order, OrderComment
from django.contrib.auth.models import User


class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ['content']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class OrderCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['date', 'client_name', 'status']
        widgets = {
            'date': DateTimeInput(),
        }