from django.db import models
from apps.courses.models import Course
from apps.teachers.models import Teacher


class Sequence(models.Model):
    """
    Séquence pédagogique : subdivision d'un cours en modules.
    Ex: Cours Python → Séquence 1 : Variables, Séquence 2 : Fonctions...
    """
    cours      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sequences')
    titre      = models.CharField(max_length=200, verbose_name="Titre")
    ordre      = models.PositiveIntegerField(default=1, verbose_name="Ordre")

    class Meta:
        verbose_name = "Séquence pédagogique"
        verbose_name_plural = "Séquences pédagogiques"
        ordering = ['cours', 'ordre']

    def __str__(self):
        return f"{self.cours.intitule} — Séq. {self.ordre} : {self.titre}"


class Resource(models.Model):
    """
    Ressource pédagogique numérique produite par un enseignant.
    Appartient à une séquence d'un cours.
    """

    class TypeResource(models.TextChoices):
        TEXTE      = 'texte',      'Contenu textuel'
        VIDEO      = 'video',      'Vidéo pédagogique'
        DOCUMENT   = 'document',   'Document pédagogique'
        QUIZ       = 'quiz',       'Quiz'
        ACTIVITE   = 'activite',   'Activité interactive'
        EVALUATION = 'evaluation', 'Évaluation'

    class Complexite(models.TextChoices):
        SIMPLE   = 'simple',   'Simple'
        MOYENNE  = 'moyenne',  'Moyenne'
        COMPLEXE = 'complexe', 'Complexe'

    sequence    = models.ForeignKey(Sequence, on_delete=models.CASCADE, related_name='resources')
    enseignant  = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='resources')
    type_ressource = models.CharField(
        max_length=20,
        choices=TypeResource.choices,
        verbose_name="Type de ressource"
    )
    titre       = models.CharField(max_length=200, verbose_name="Titre")
    complexite  = models.CharField(
        max_length=20,
        choices=Complexite.choices,
        default=Complexite.MOYENNE,
        verbose_name="Complexité"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ressource pédagogique"
        verbose_name_plural = "Ressources pédagogiques"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} ({self.get_type_ressource_display()})"