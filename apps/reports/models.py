from django.db import models
from apps.teachers.models import Teacher


class Report(models.Model):
    """
    État récapitulatif généré pour un enseignant sur une période.
    Stocke le total des heures et le montant à payer.
    """

    class TypeReport(models.TextChoices):
        INDIVIDUEL  = 'individuel',  'Fiche individuelle'
        GLOBAL      = 'global',      'État global'
        PAIEMENT    = 'paiement',    'État de paiement'
        STATISTIQUE = 'statistique', 'Statistiques pédagogiques'

    enseignant       = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reports',
        verbose_name="Enseignant"
    )
    type_report      = models.CharField(max_length=20, choices=TypeReport.choices)
    annee_academique = models.CharField(max_length=9, verbose_name="Année académique")
    total_heures     = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    montant_total    = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_generation  = models.DateTimeField(auto_now_add=True)
    genere_par       = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Généré par"
    )

    class Meta:
        verbose_name = "Rapport"
        verbose_name_plural = "Rapports"
        ordering = ['-date_generation']

    def __str__(self):
        return f"{self.get_type_report_display()} — {self.annee_academique}"