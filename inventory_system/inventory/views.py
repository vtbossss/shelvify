from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Inventory
from .serializers import UserSerializer, InventorySerializer
from .permissions import IsAdmin, IsManager, IsStaff
from .forms import InventoryForm, UserForm

# User Management View (API)
class UserManagementView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
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

# Inventory View (API)
class InventoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Admin can view all items, Managers and Staff can view their section
        if request.user.role == 'Admin':
            items = Inventory.objects.all()
        elif request.user.role == 'Manager':
            items = Inventory.objects.filter(section=request.user.username)  # Can filter by section
        else:
            items = Inventory.objects.filter(section=request.user.username)  # Same for Staff
        serializer = InventorySerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'Admin':
            return Response({'error': 'Only Admins can add inventory items'}, status=403)
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.role != 'Admin':
            return Response({'error': 'Only Admins can delete items'}, status=403)
        try:
            item = Inventory.objects.get(pk=pk)
            item.delete()
            return Response({'message': 'Item deleted successfully!'})
        except Inventory.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)

# Login View
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

# User Management (Admin-only view)
def user_management_view(request):
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return redirect('permission_denied')
    
    users = User.objects.all()
    return render(request, 'inventory/user_management.html', {'users': users, 'user': request.user})

# Inventory List (View for all users)
def inventory_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.role == 'Admin':
        items = Inventory.objects.all()
    elif request.user.role == 'Manager' or request.user.role == 'Staff':
        items = Inventory.objects.filter(section=request.user.username)
    
    return render(request, 'inventory/inventory_list.html', {
        'inventory_items': items,
        'user': request.user  # Pass the user object to the template for role-based logic
    })

# Add Inventory (Admin-only view)
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

# Logout View (Clears JWT cookies)
def logout_view(request):
    if request.user.is_authenticated:
        # Clear the session (if using session-based auth)
        django_logout(request)  # This clears the Django session
        
        response = redirect('login')
        response.delete_cookie('access_token')  # Delete access token cookie
        response.delete_cookie('refresh_token')  # Delete refresh token cookie
        return response
    return redirect('login')

# Home View (Displays information based on user role)
def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated
    
    # Logic for different roles
    if request.user.role == 'Admin':
        # Admin sees a full overview of users and inventory
        total_users = User.objects.count()
        total_inventory_items = Inventory.objects.count()
        return render(request, 'inventory/home.html', {
            'role': 'Admin',
            'total_users': total_users,
            'total_inventory_items': total_inventory_items,
            'user': request.user  # Pass the user object to the template
        })
    
    elif request.user.role == 'Manager':
        # Manager sees their assigned inventory items
        managed_inventory = Inventory.objects.filter(section=request.user.username)
        return render(request, 'inventory/home.html', {
            'role': 'Manager',
            'managed_inventory': managed_inventory,
            'user': request.user  # Pass the user object to the template
        })
    
    elif request.user.role == 'Staff':
        # Staff sees a filtered view of inventory items for their section
        section_inventory = Inventory.objects.filter(section=request.user.username)
        return render(request, 'inventory/home.html', {
            'role': 'Staff',
            'section_inventory': section_inventory,
            'user': request.user  # Pass the user object to the template
        })
    
    else:
        # If the role is unexpected, redirect to login
        return redirect('login')


# Edit User View
def edit_user(request, user_id):
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return redirect('permission_denied')  # Redirect if not an admin
    
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

# Delete User View
def delete_user(request, user_id):
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return redirect('permission_denied')  # Redirect if not an admin
    
    try:
        user = get_object_or_404(User, id=user_id)  # Fetch user by ID
        user.delete()  # Delete user
        messages.success(request, 'User deleted successfully.')
        return redirect('user_management_template')  # Redirect to user management page
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('user_management_template')  # Redirect to user management page
