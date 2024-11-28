from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ==============================
    # Template Views (Frontend)
    # ==============================

    # Homepage route
    path('', views.home_view, name='home'),

    # User Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User Management (Admin-only templates)
    path('users/', views.user_management_view, name='user_management_template'),
    path('user/edit/<int:user_id>/', views.edit_user, name='edit_user'),  # Template view for editing user
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),  # Template view for deleting user

    # Inventory Management (Templates)
    path('inventory/', views.inventory_list_view, name='inventory_list'),
    path('inventory/add/', views.add_inventory_view, name='add_inventory'),
    path('inventory/edit/<int:item_id>/', views.edit_inventory_view, name='edit_inventory'),
    path('inventory/delete/<int:item_id>/', views.delete_inventory_view, name='delete_inventory'),

    # ==============================
    # API Views (Backend)
    # ==============================

    # User Management APIs
    path('api/users/', views.UserManagementView.as_view(), name='user_management_api'),
    path('api/users/<int:pk>/', views.UserManagementView.as_view(), name='user_detail_api'),

    # Inventory APIs
    path('api/inventory/', views.InventoryView.as_view(), name='inventory_api'),
    path('api/inventory/<int:pk>/', views.InventoryView.as_view(), name='inventory_detail_api'),

    # JWT Token Routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
