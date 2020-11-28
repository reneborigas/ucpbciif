from django.urls import path
from .api import LoginView, LogoutView,CheckAuthentication

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('checkauth/', CheckAuthentication.as_view()),
    
    # path('validatepassword/',ValidatePassword.as_view())
]
