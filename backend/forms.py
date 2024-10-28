from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        # fields = ['email', 'username', 'phone_number', 'password',] # Add all necessary fields here

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance and self.instance.pk:
    #         self.fields['email'].required = False