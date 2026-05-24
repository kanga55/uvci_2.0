from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé.
    On étend AbstractUser pour ajouter le champ 'role'.
    AbstractUser nous donne déjà : username, email, password,
    first_name, last_name, is_active, is_staff, date_joined.
    """

    class Role(models.TextChoices):
        ADMIN       = 'admin',       'Administrateur'
        SECRETAIRE  = 'secretaire',  'Secrétaire Principal'
        ENSEIGNANT  = 'enseignant',  'Enseignant'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ENSEIGNANT,
        verbose_name="Rôle"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Adresse email"
    )

    # On utilise l'email comme identifiant de connexion
    USERNAME_FIELD = 'email'

    # Ces champs sont demandés lors de createsuperuser
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    # --- Propriétés utiles pour les vues et permissions ---

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_secretaire(self):
        return self.role == self.Role.SECRETAIRE

    @property
    def is_enseignant(self):
        return self.role == self.Role.ENSEIGNANT