from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Sérialise un utilisateur pour l'API.
    On exclut le mot de passe des données retournées.
    """

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'role', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class LoginSerializer(serializers.Serializer):
    """
    Valide les données de connexion (email + mot de passe).
    """
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        authenticate() vérifie email + mot de passe dans la base.
        Si c'est bon, il retourne l'objet User.
        Si c'est mauvais, il retourne None.
        """
        user = authenticate(
            request=self.context.get('request'),
            username=data['email'],   # USERNAME_FIELD = email
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError(
                "Email ou mot de passe incorrect."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Ce compte est désactivé."
            )

        data['user'] = user
        return data


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Crée un nouvel utilisateur.
    Réservé à l'administrateur.
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name',
            'role', 'password'
        ]

    def create(self, validated_data):
        # create_user() hashe automatiquement le mot de passe
        user = User.objects.create_user(**validated_data)
        return user