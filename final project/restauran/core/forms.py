from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CardInfo
from .models import TableBooking
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'preparation_time', 'is_in_stop_list']

class ClientRegistrationForm(UserCreationForm):
    card_number = forms.CharField(max_length=16)
    expiry_date = forms.CharField(max_length=5)
    cardholder_name = forms.CharField(max_length=100)
    cvv = forms.CharField(max_length=3)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CLIENT
        if commit:
            user.save()
            CardInfo.objects.create(
                client=user,
                card_number=self.cleaned_data['card_number'],
                expiry_date=self.cleaned_data['expiry_date'],
                cardholder_name=self.cleaned_data['cardholder_name'],
                cvv=self.cleaned_data['cvv'],
            )
        return user


class TableBookingForm(forms.ModelForm):
    class Meta:
        model = TableBooking
        fields = ['client', 'table', 'date', 'time', 'number_of_people', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'status': forms.Select(),
        }

class ClientBookingForm(forms.ModelForm):
    class Meta:
        model = TableBooking
        fields = ['table', 'date', 'time', 'number_of_people']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

