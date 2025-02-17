from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, HealthReportSerializer
from .models import HealthReport
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import exception_handler


# Function to render login page
def login_page(request):
    return render(request, 'login.html')



# Function to render register page
def register_page(request):
    return render(request, 'register.html')

# Function to render health report page
def health_page(request):
    return render(request, 'health.html')


@api_view(['GET'])
def api_home(request):
    return JsonResponse({
        "message": "Welcome to the Health Report API!",
        "register": "/api/register/",
        "login": "/api/login/",
        "refresh_token": "/api/token/refresh/",
        "health_reports": "/api/health-reports/"
    })
User = get_user_model()

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['error'] = str(exc)  # ✅ Convert exception to JSON response
    return response

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Login successful"
            })
        return Response({"detail": "Incorrect email or password"}, status=status.HTTP_401_UNAUTHORIZED)





class HealthReportView(generics.ListCreateAPIView):
    queryset = HealthReport.objects.all()
    serializer_class = HealthReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print("🔹 Request User:", self.request.user)  # ✅ Check if Django recognizes the user

        if not self.request.user or self.request.user.is_anonymous:
            print("🔴 User is not authenticated!")
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer.save(user=self.request.user)




class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

class HealthReportListCreateView(generics.ListCreateAPIView):
    serializer_class = HealthReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HealthReport.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
