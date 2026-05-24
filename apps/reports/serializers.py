from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    enseignant_nom = serializers.CharField(
        source='enseignant.get_full_name', read_only=True
    )
    type_label = serializers.CharField(
        source='get_type_report_display', read_only=True
    )

    class Meta:
        model  = Report
        fields = [
            'id', 'type_report', 'type_label',
            'enseignant', 'enseignant_nom',
            'annee_academique', 'total_heures',
            'montant_total', 'date_generation', 'genere_par'
        ]
        read_only_fields = [
            'id', 'date_generation',
            'enseignant_nom', 'type_label'
        ]