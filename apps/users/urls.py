from django.urls import path
from .views import UserRegisterView, ManageUserView, LogoutView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('me/', ManageUserView.as_view(), name='manage-user'),
    path('logout/', LogoutView.as_view(), name='logout'),
]