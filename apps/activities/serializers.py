from rest_framework import serializers
from .models import Activity, AnneeAcademique


class AnneeAcademiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AnneeAcademique
        fields = ['id', 'libelle', 'en_cours', 'date_debut', 'date_fin']


class ActivitySerializer(serializers.ModelSerializer):
    enseignant_nom   = serializers.CharField(source='enseignant.get_full_name', read_only=True)
    resource_titre   = serializers.CharField(source='resource.titre', read_only=True)
    type_label       = serializers.CharField(source='get_type_activite_display', read_only=True)

    class Meta:
        model  = Activity
        fields = [
            'id', 'enseignant', 'enseignant_nom',
            'resource', 'resource_titre',
            'type_activite', 'type_label',
            'heures', 'annee_academique',
            'date_activite', 'commentaire', 'date_creation'
        ]
        read_only_fields = [
            'id', 'heures', 'date_creation',
            'enseignant_nom', 'resource_titre', 'type_label'
        ]

    def validate(self, data):
        """
        Vérifie que l'enseignant de l'activité
        est bien l'enseignant lié à la ressource.
        """
        enseignant = data.get('enseignant')
        resource   = data.get('resource')
        if enseignant and resource:
            if resource.enseignant != enseignant:
                raise serializers.ValidationError(
                    "L'enseignant ne correspond pas à celui de la ressource."
                )
        return data