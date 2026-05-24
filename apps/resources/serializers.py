from rest_framework import serializers
from .models import Sequence, Resource


class SequenceSerializer(serializers.ModelSerializer):
    cours_intitule = serializers.CharField(source='cours.intitule', read_only=True)

    class Meta:
        model  = Sequence
        fields = ['id', 'cours', 'cours_intitule', 'titre', 'ordre']
        read_only_fields = ['id', 'cours_intitule']


class ResourceSerializer(serializers.ModelSerializer):
    sequence_titre   = serializers.CharField(source='sequence.titre', read_only=True)
    enseignant_nom   = serializers.CharField(source='enseignant.get_full_name', read_only=True)
    type_label       = serializers.CharField(source='get_type_ressource_display', read_only=True)
    complexite_label = serializers.CharField(source='get_complexite_display', read_only=True)

    class Meta:
        model  = Resource
        fields = [
            'id', 'titre', 'type_ressource', 'type_label',
            'complexite', 'complexite_label',
            'sequence', 'sequence_titre',
            'enseignant', 'enseignant_nom',
            'date_creation', 'date_modification'
        ]
        read_only_fields = [
            'id', 'date_creation', 'date_modification',
            'sequence_titre', 'enseignant_nom',
            'type_label', 'complexite_label'
        ]