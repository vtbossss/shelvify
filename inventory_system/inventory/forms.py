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


from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # Add other fields as needed

    # Override the save method to assign the default role as 'Staff'
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'Staff'  # Set the default role as Staff
        user.set_password(self.cleaned_data['password'])  # Hash the password

        # If 'email' is included, assign it
        if 'email' in self.cleaned_data:
            user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

    # Validate the confirm password field
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Password confirmation check
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Check if username or email already exists
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")

        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email address already exists.")

        return cleaned_data
