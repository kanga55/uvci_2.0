from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    department_nom = serializers.CharField(
        source='department.nom', read_only=True
    )

    class Meta:
        model = Course
        fields = [
            'id', 'intitule', 'filiere', 'niveau', 'semestre',
            'nombre_heures', 'credits', 'department', 'department_nom',
            'date_creation'
        ]
        read_only_fields = ['id', 'date_creation', 'department_nom']