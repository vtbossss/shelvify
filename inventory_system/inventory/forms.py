from django import forms
from .models import Inventory
from django.contrib.auth import get_user_model
User = get_user_model()

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'quantity', 'section']

from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']  # Fields you want to allow admins to edit


from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'Staff'  # Set default role as Staff
        user.set_password(self.cleaned_data['password'])  # Hash the password

        # If 'email' is included, assign it
        if 'email' in self.cleaned_data:
            user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

    # Validate the form fields
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        # Check if passwords match
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email address already exists.")

        # Validate password length
        self.validate_password_length(password)

        return cleaned_data

    # Custom password length validation
    def validate_password_length(self, password):
        # Check length: Minimum 8 characters
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        return password

    # Optionally, you can validate if the username is alphanumeric and meets minimum length requirements
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        
        if not username.isalnum():
            raise ValidationError("Username can only contain letters and numbers.")

        return username

    # Optionally, validate the email format if necessary
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Simple email validation is already handled by Django's EmailField, but you can extend it if needed.
        return email