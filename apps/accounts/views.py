from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import login, logout
from .serializers import LoginSerializer, UserSerializer, CreateUserSerializer
from .models import User


class LoginView(APIView):
    """
    POST /api/accounts/login/
    Corps : { "email": "...", "password": "..." }
    Retourne les infos de l'utilisateur connecté.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # crée la session Django

            return Response({
                'message': 'Connexion réussie.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    """
    POST /api/accounts/logout/
    Détruit la session de l'utilisateur.
    """
    def post(self, request):
        logout(request)
        return Response(
            {'message': 'Déconnexion réussie.'},
            status=status.HTTP_200_OK
        )


class MeView(APIView):
    """
    GET /api/accounts/me/
    Retourne les infos de l'utilisateur actuellement connecté.
    Utilisé par le frontend pour savoir quel dashboard afficher.
    """
    def get(self, request):
        return Response(
            UserSerializer(request.user).data,
            status=status.HTTP_200_OK
        )


class UserListCreateView(APIView):
    """
    GET  /api/accounts/users/  → liste tous les utilisateurs
    POST /api/accounts/users/  → crée un utilisateur
    Réservé à l'administrateur uniquement.
    """
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get(self, request):
        if not request.user.is_admin:
            return Response(
                {'detail': 'Accès refusé.'},
                status=status.HTTP_403_FORBIDDEN
            )

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {'detail': 'Accès refusé.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

from django.middleware.csrf import get_token
from django.http import JsonResponse

class CSRFTokenView(APIView):
    """
    GET /api/accounts/csrf/
    Retourne un cookie csrftoken au navigateur.
    Le frontend l'utilise pour les requêtes POST.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = get_token(request)
        return JsonResponse({'csrfToken': token})
    

from django.middleware.csrf import get_token
from django.http import JsonResponse

class CSRFTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = get_token(request)
        return JsonResponse({'csrfToken': token})