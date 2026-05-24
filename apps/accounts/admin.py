from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    On personnalise l'interface d'administration Django
    pour afficher et modifier le champ 'role'.
    """

    # Colonnes affichées dans la liste des utilisateurs
    list_display = [
        'email', 'first_name', 'last_name',
        'role', 'is_active', 'date_joined'
    ]

    list_filter = ['role', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['last_name']

    # Ajouter 'role' dans le formulaire de modification
    fieldsets = UserAdmin.fieldsets + (
        ('Rôle UVCI', {'fields': ('role',)}),
    )

    # Ajouter 'role' dans le formulaire de création
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rôle UVCI', {'fields': ('role',)}),
    )