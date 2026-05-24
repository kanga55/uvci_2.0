from django.contrib import admin
from .models import Activity, AnneeAcademique


@admin.register(AnneeAcademique)
class AnneeAcademiqueAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'en_cours', 'date_debut', 'date_fin']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display  = ['enseignant', 'resource', 'type_activite', 'heures', 'annee_academique', 'date_activite']
    list_filter   = ['type_activite', 'annee_academique']
    search_fields = ['enseignant__nom', 'enseignant__prenom']
    readonly_fields = ['heures']