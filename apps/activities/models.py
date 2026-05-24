from django.db import models
from apps.teachers.models import Teacher
from apps.resources.models import Resource


class Activity(models.Model):
    """
    Activité pédagogique d'un enseignant : création ou mise à jour d'une ressource.
    C'est ici que les heures sont calculées automatiquement selon les règles de l'UVCI.
    """

    class TypeActivite(models.TextChoices):
        CREATION    = 'creation',    'Création de ressource'
        MISE_A_JOUR = 'mise_a_jour', 'Mise à jour de ressource'

    # Barème horaire selon le type et la complexité (en heures)
    BAREME = {
        'creation': {
            'simple':   2.0,
            'moyenne':  4.0,
            'complexe': 6.0,
        },
        'mise_a_jour': {
            'simple':   0.5,
            'moyenne':  1.0,
            'complexe': 2.0,
        },
    }

    enseignant     = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='activities')
    resource       = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='activities')
    type_activite  = models.CharField(
        max_length=20,
        choices=TypeActivite.choices,
        verbose_name="Type d'activité"
    )
    # Heures calculées automatiquement lors de la sauvegarde
    heures         = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name="Heures attribuées"
    )
    annee_academique = models.CharField(
        max_length=9,
        verbose_name="Année académique",
        help_text="Format : 2025-2026"
    )
    date_activite  = models.DateField(verbose_name="Date de l'activité")
    commentaire    = models.TextField(blank=True, verbose_name="Commentaire")
    date_creation  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Activité pédagogique"
        verbose_name_plural = "Activités pédagogiques"
        ordering = ['-date_activite']

    def save(self, *args, **kwargs):
        """
        Calcul automatique des heures avant chaque sauvegarde.
        On lit la complexité depuis la ressource liée,
        puis on applique le barème selon le type d'activité.
        """
        complexite = self.resource.complexite
        type_acte  = self.type_activite
        self.heures = self.BAREME.get(type_acte, {}).get(complexite, 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.enseignant} — {self.get_type_activite_display()} — {self.heures}h"


class AnneeAcademique(models.Model):
    """
    Paramètre global : année académique en cours.
    L'administrateur la définit une fois, elle est utilisée partout.
    """
    libelle    = models.CharField(max_length=9, unique=True, verbose_name="Libellé (ex: 2025-2026)")
    en_cours   = models.BooleanField(default=False, verbose_name="Année en cours")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin   = models.DateField(verbose_name="Date de fin")

    class Meta:
        verbose_name = "Année académique"
        verbose_name_plural = "Années académiques"

    def save(self, *args, **kwargs):
        # Une seule année peut être "en cours" à la fois
        if self.en_cours:
            AnneeAcademique.objects.exclude(pk=self.pk).update(en_cours=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle