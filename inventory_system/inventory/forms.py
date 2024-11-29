from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Inventory

User = get_user_model()  # Retrieve the custom user model

# Form for Inventory model
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'quantity', 'section']  # Fields to be included in the form

# Form for User model to edit user details (admin only)
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']  # Fields admins can modify

# Registration form for creating new users
class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')  # Confirm password field

    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # Fields for user registration

    # Save method for setting hashed password and default role securely
    def save(self, commit=True):
        user = super().save(commit=False)  # Prevent immediate saving to ensure password is hashed
        user.role = 'Staff'  # Default role set to 'Staff' to restrict initial access
        user.set_password(self.cleaned_data['password'])  # Hash the password securely using Django's built-in method

        # Assign email securely if provided
        if 'email' in self.cleaned_data:
            user.email = self.cleaned_data['email']

        if commit:
            user.save()  # Save the user to the database after password has been securely handled
        return user

    # Custom validation for ensuring secure form submission
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        # Ensure passwords match for account security
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Ensure the username is unique to prevent unauthorized account creation
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")

        # Check if the email is already in use to prevent account duplication
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email address already exists.")

        # Validate password length for better security (minimum 8 characters)
        self.validate_password_length(password)

        return cleaned_data

    # Password length validation to enforce minimum security standards
    def validate_password_length(self, password):
        # Ensure that password meets the minimum security length of 8 characters
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password

    # Username validation to ensure a secure format and prevent easily guessable usernames
    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Enforce a minimum length to avoid trivial usernames
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        
        # Allow only alphanumeric usernames to prevent special characters which could be exploited
        if not username.isalnum():
            raise ValidationError("Username can only contain letters and numbers.")

        return username

    # Optional: Validate email format if necessary; Django's EmailField already provides basic validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
