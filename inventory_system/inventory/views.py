from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Inventory
from .serializers import UserSerializer, InventorySerializer
from .permissions import IsAdmin, IsManager, IsStaff
from .forms import InventoryForm, UserForm, RegistrationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


# Get the User model
User = get_user_model()


# User Management View (API) - Admin can view and update roles
class UserManagementView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """ Get all users """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        """ Update user's role (only Admin can do this) """
        try:
            user = User.objects.get(pk=pk)
            new_role = request.data.get('role', user.role)
            # Validate the role change
            if new_role not in ['Admin', 'Manager', 'Staff']:
                return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.role = new_role
            user.save()
            return Response({'message': 'Role updated successfully!'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# Inventory View (API) - View, add, update, or delete inventory items
class InventoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ View inventory items for Admin, Manager, or Staff """
        if request.user.role in ['Admin', 'Manager', 'Staff']:
            items = Inventory.objects.all()
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = InventorySerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Add inventory item (only Admin) """
        if request.user.role != 'Admin':
            return Response({'error': 'Only Admins can add inventory items'}, status=status.HTTP_403_FORBIDDEN)

        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """ Update inventory item (Admin/Manager only) """
        if request.user.role not in ['Admin', 'Manager']:
            return Response({'error': 'Only Admins and Managers can update items'}, status=status.HTTP_403_FORBIDDEN)

        try:
            item = Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure Managers cannot modify restricted fields
        if request.user.role == 'Manager' and 'updated_by' in request.data:
            return Response({'error': 'Managers cannot modify the "updated_by" field'}, status=status.HTTP_403_FORBIDDEN)

        serializer = InventorySerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """ Delete inventory item (only Admin) """
        if request.user.role != 'Admin':
            return Response({'error': 'Only Admins can delete items'}, status=status.HTTP_403_FORBIDDEN)

        try:
            item = Inventory.objects.get(pk=pk)
            item.delete()
            return Response({'message': 'Item deleted successfully!'})
        except Inventory.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


# Login View - Authenticate user and set JWT tokens in cookies
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Set JWT tokens as HttpOnly cookies
            response = redirect('home')  # Redirect to the home page
            response.set_cookie('access_token', access_token, httponly=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
            return response
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return render(request, 'inventory/login.html')


# User Management View (Admin-only) - List all users
def user_management_view(request):
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return redirect('permission_denied')

    users = User.objects.all()
    return render(request, 'inventory/user_management.html', {'users': users, 'user': request.user})


# Inventory List View - View inventory based on user role
def inventory_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role == 'Admin':
        items = Inventory.objects.all()
    elif request.user.role in ['Manager', 'Staff']:
        items = Inventory.objects.all()

    return render(request, 'inventory/inventory_list.html', {
        'inventory_items': items,
        'user': request.user  # Pass the user object to the template for role-based logic
    })


# Add Inventory View - Add inventory item (only Admin)
def add_inventory_view(request):
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return redirect('permission_denied')

    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()

    return render(request, 'inventory/add_inventory.html', {'form': form, 'user': request.user})


# Logout View - Clears JWT cookies
def logout_view(request):
    if request.user.is_authenticated:
        django_logout(request)  # Clears the Django session

        response = redirect('login')
        response.delete_cookie('access_token')  # Delete access token cookie
        response.delete_cookie('refresh_token')  # Delete refresh token cookie
        return response
    return redirect('login')


# Home View - Displays information based on user role
def home_view(request):
    if not request.user.is_authenticated:
        return render(request, 'inventory/basichome.html')  # Redirect to login if not authenticated

    # Logic for different roles
    if request.user.role == 'Admin':
        total_users = User.objects.count()
        total_inventory_items = Inventory.objects.count()
        return render(request, 'inventory/home.html', {
            'role': 'Admin',
            'total_users': total_users,
            'total_inventory_items': total_inventory_items,
            'user': request.user
        })
    elif request.user.role == 'Manager':
        managed_inventory = Inventory.objects.all()
        total_inventory_items = Inventory.objects.count()
        return render(request, 'inventory/home.html', {
            'role': 'Manager',
            'managed_inventory': managed_inventory,
            'total_inventory_items': total_inventory_items,
            'user': request.user
        })
    elif request.user.role == 'Staff':
        staff_inventory = Inventory.objects.all()
        return render(request, 'inventory/home.html', {
            'role': 'Staff',
            'section_inventory': staff_inventory,
            'user': request.user
        })
    else:
        return redirect('login')


# Edit User View - Edit user (Admin only)
def edit_user(request, user_id):
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return redirect('permission_denied')

    user = get_object_or_404(User, id=user_id)  # Fetch user by ID
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)  # Bind form to existing user instance
        if form.is_valid():
            form.save()  # Save the updated user data
            messages.success(request, 'User updated successfully.')
            return redirect('user_management_template')  # Redirect to user management page
    else:
        form = UserForm(instance=user)  # Display form with existing data

    return render(request, 'inventory/edit_user.html', {'form': form, 'user': user})


# Delete User View - Admin can delete users
def delete_user(request, user_id):
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return redirect('permission_denied')

    try:
        user = get_object_or_404(User, id=user_id)  # Fetch user by ID
        user.delete()  # Delete user
        messages.success(request, 'User deleted successfully.')
        return redirect('user_management_template')  # Redirect to user management page
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('user_management_template')  # Redirect to user management page


# Edit Inventory View - Admin and Manager can edit inventory items
@login_required
def edit_inventory_view(request, item_id):
    if request.user.role not in ['Admin', 'Manager']:
        return redirect('permission_denied')

    inventory_item = get_object_or_404(Inventory, id=item_id)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory_item)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm(instance=inventory_item)

    return render(request, 'inventory/edit_inventory.html', {'form': form, 'inventory_item': inventory_item})


# Permissions - Page for denying permission access
def permission_denied(request):
    return render(request, 'inventory/permission_denied.html')

@login_required
def delete_inventory_view(request, item_id):
    if request.user.role != 'Admin':
        return redirect('inventory_list')  # Only Admins can delete

    item = get_object_or_404(Inventory, id=item_id)
    if request.method == 'POST':  # Confirm deletion
        item.delete()
        return redirect('inventory_list')

    return render(request, 'inventory/delete_inventory.html', {'item': item})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # The form already handles saving and setting the password
            
            messages.success(request, f'User {user.username} created successfully. You can update the role from the admin panel.')
            
            # Redirect to login page or another page after successful registration
            return redirect('login')  # Change 'login' to the appropriate URL name for your login page
        else:
            # If the form is not valid, it will automatically show the errors in the template
            messages.error(request, 'There was an error with the registration form.')
    else:
        form = RegistrationForm()

    return render(request, 'inventory/register.html', {'form': form})

