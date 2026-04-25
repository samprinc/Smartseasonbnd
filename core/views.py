from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import Field, FieldUpdate
from .serializers import FieldSerializer, FieldUpdateSerializer
from .permissions import IsAdminOrAgent
# Add this to the bottom of core/views.py
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Allows admins to see the team roster"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrAgent]

# --- Authentication ---
class CustomLoginView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]
    
    def post(self, request):

        print(f"DEBUG: Content-Type header: {request.content_type}")
        print(f"DEBUG: Raw Request Data: {request.data}")

        username = request.data.get('username')
        password = request.data.get('password')

        print(f"DEBUG: Attempting login for user: {username} with password: {password}")

        user = authenticate(username=username, password=password)
        
        print(f"DEBUG: Authenticate result: {user}")

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# --- Field Management ---
class FieldViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSerializer
    permission_classes = [IsAdminOrAgent]

    def get_queryset(self):
        user = self.request.user
        # Admins view all fields 
        if user.is_staff or user.role == 'admin':
            return Field.objects.all()
        # Agents see their assigned fields 
        return Field.objects.filter(assigned_to=user)

# --- Update Tracking ---
class FieldUpdateViewSet(viewsets.ModelViewSet):
    serializer_class = FieldUpdateSerializer
    permission_classes = [IsAdminOrAgent]

    def get_queryset(self):
        user = self.request.user
        # Admins monitor all updates across agents [cite: 32]
        if user.is_staff or user.role == 'admin':
            return FieldUpdate.objects.all()
        # Agents see updates for their assigned fields [cite: 27, 49]
        return FieldUpdate.objects.filter(field__assigned_to=user)