from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework import status, views
from rest_framework.response import Response
from .serializers import UserSerializer


# class ValidatePassword(views.APIView):
    
#     @method_decorator(csrf_protect)

#     def get_object(self, queryset=None):
#         return self.request.user

#     def put(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = ChangePasswordSerializer(data=request.data)

#         if serializer.is_valid():
#             old_password = serializer.data.get("old_password")
#             if not self.object.check_password(old_password):
#                 return Response({"old_password": ["Wrong password."]}, 
#                                 status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    
    @method_decorator(csrf_protect)
    def post(self,request):
  
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"))
        
        if user is None or not user.is_active:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username or Password is Incorrect'
            },status= status.HTTP_401_UNAUTHORIZED)
        
        login(request, user)
        return Response(UserSerializer(user).data)

class LogoutView(views.APIView):
    def get(self, request):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)