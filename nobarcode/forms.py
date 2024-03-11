from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

from .models import ExcelFile

from .models import RequestInfo

class RequestInfoForm(forms.ModelForm):
    class Meta:
        model = RequestInfo
        fields = '__all__'

# class RequestInfoForm(forms.ModelForm):
#     class Meta:
#         model = RequestInfo
#         fields = ['request_number', 'quantity', 'order']  # Add other fields

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         # Tắt autocomplete cho từng trường cụ thể bằng cách đặt thuộc tính name và id
#         self.fields['request_number'].widget.attrs.update({'autocomplete': 'off', 'id': 'no_autocomplete_request_number', 'name': 'no_autocomplete_request_number'})
#         self.fields['quantity'].widget.attrs.update({'autocomplete': 'off', 'id': 'no_autocomplete_quantity', 'name': 'no_autocomplete_quantity'})
#         self.fields['order'].widget.attrs.update({'autocomplete': 'off', 'id': 'no_autocomplete_order', 'name': 'no_autocomplete_order'})


class ExcelFileForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ['file']






# from .models import Drawing

# class DrawingForm(forms.ModelForm):
#     class Meta:
#         model = Drawing
#         fields = ['pdf']




class UserRegistrationForm(UserCreationForm):

    # username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'MSNV'}))
    username = forms.IntegerField(
        label='MSNV',  # Change the label to 'MSNV'
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'MSNV'}),  # Change the placeholder to 'MSNV'
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Confirm Password'}))

    full_name = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Họ và tên'}),
    )

    class Meta:
        model = User  
        # fields = ['username', 'password1', 'password2']
        fields = ['username', 'password1', 'password2', 'full_name']



class UserLoginForm(forms.Form):
    username = forms.IntegerField(
        label='MSNV',  
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'MSNV'}),  # Change the placeholder to 'MSNV'
    )

    # username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}))


