from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display  = ['type_report', 'enseignant', 'annee_academique', 'total_heures', 'montant_total', 'date_generation']
    list_filter   = ['type_report', 'annee_academique']