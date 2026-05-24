from django.db import models
from apps.teachers.models import Department


class Course(models.Model):
    """
    Cours dispensé à l'UVCI.
    Associé à une filière, un niveau et un semestre.
    """

    class Niveau(models.TextChoices):
        L1 = 'L1', 'Licence 1'
        L2 = 'L2', 'Licence 2'
        L3 = 'L3', 'Licence 3'
        M1 = 'M1', 'Master 1'
        M2 = 'M2', 'Master 2'

    class Semestre(models.TextChoices):
        S1 = 'S1', 'Semestre 1'
        S2 = 'S2', 'Semestre 2'

    intitule      = models.CharField(max_length=200, verbose_name="Intitulé")
    filiere       = models.CharField(max_length=100, verbose_name="Filière")
    niveau        = models.CharField(max_length=5, choices=Niveau.choices, verbose_name="Niveau")
    semestre      = models.CharField(max_length=5, choices=Semestre.choices, verbose_name="Semestre")
    nombre_heures = models.PositiveIntegerField(verbose_name="Nombre d'heures")
    credits       = models.PositiveIntegerField(verbose_name="Crédits")
    department    = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name="Département"
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['filiere', 'niveau', 'intitule']

    def __str__(self):
        return f"{self.intitule} ({self.niveau} - {self.semestre})"