from django.db import models


class Department(models.Model):
    """Département universitaire (ex: Informatique, Mathématiques...)"""

    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom")

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Teacher(models.Model):
    """
    Enseignant de l'UVCI.
    Lié à un département, avec grade, statut et taux horaire.
    """

    class Grade(models.TextChoices):
        ASSISTANT         = 'assistant',          'Assistant'
        MAITRE_ASSISTANT  = 'maitre_assistant',   'Maître-Assistant'
        PROFESSEUR        = 'professeur',         'Professeur'

    class Statut(models.TextChoices):
        PERMANENT  = 'permanent',  'Permanent'
        VACATAIRE  = 'vacataire',  'Vacataire'

    nom        = models.CharField(max_length=100, verbose_name="Nom")
    prenom     = models.CharField(max_length=100, verbose_name="Prénom")
    email      = models.EmailField(unique=True, verbose_name="Email")
    telephone  = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    grade      = models.CharField(max_length=20, choices=Grade.choices, verbose_name="Grade")
    statut     = models.CharField(max_length=20, choices=Statut.choices, verbose_name="Statut")
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name='teachers',
        verbose_name="Département"
    )
    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Taux horaire (FCFA)"
    )
    # Lien optionnel vers le compte utilisateur de l'enseignant
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teacher_profile',
        verbose_name="Compte utilisateur"
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.get_grade_display()})"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"