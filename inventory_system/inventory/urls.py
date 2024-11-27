from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Homepage route
    path('', views.home_view, name='home'),

    # User authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User management (Admin access)
    path('users/', views.user_management_view, name='user_management_template'),
    path('user/edit/<int:user_id>/', views.edit_user, name='edit_user'),  # Added edit user route
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),  # Added delete user route

    # Inventory management
    path('inventory/', views.inventory_list_view, name='inventory_list'),
    path('inventory/add/', views.add_inventory_view, name='add_inventory'),

    # API Views (for interacting with the backend)
    path('api/users/', views.UserManagementView.as_view(), name='user_management'),
    path('api/inventory/', views.InventoryView.as_view(), name='inventory'),
    path('api/inventory/<int:pk>/', views.InventoryView.as_view(), name='inventory_detail'),

    # JWT Token routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
