
#AuthenticationForm check validation username and pss.
# pass, because no need to write extra logic bocaise of AuthenticationForm.
# This file contains registration and login forms.
# Django handles form validation and password security.




# This file contains registration, login and other application forms.
# Django handles form validation and password security.

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Group, Message, UserProfile


# Registration Form

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    mobile_number = forms.CharField(
        max_length=15,
        required=True,
        label="Mobile Number",
        help_text="Enter your mobile number with country code if needed."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_mobile_number(self):

        mobile = self.cleaned_data['mobile_number'].strip()
        mobile = mobile.replace(" ", "").replace("-", "")

        if not mobile.lstrip("+").isdigit() or not (7 <= len(mobile.lstrip("+")) <= 15):
            raise forms.ValidationError(
                "Enter a valid mobile number."
            )

        if UserProfile.objects.filter(mobile_number=mobile).exists():
            raise forms.ValidationError(
                "This mobile number is already registered."
            )

        return mobile


# Login Form

class LoginForm(AuthenticationForm):

    pass


# Create Group Form

class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name', 'description']


# Add Members Form

class AddMemberForm(forms.Form):

    search_query = forms.CharField(
        max_length=150,
        required=True,
        label="Username or Mobile Number",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username or mobile number'
        })
    )


# Message Form

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your message here...'
            })
        }
