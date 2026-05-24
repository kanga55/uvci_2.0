from rest_framework import serializers
from .models import Teacher, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'nom']


class TeacherSerializer(serializers.ModelSerializer):
    department_nom = serializers.CharField(
        source='department.nom', read_only=True
    )
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = [
            'id', 'nom', 'prenom', 'full_name', 'email', 'telephone',
            'grade', 'statut', 'department', 'department_nom',
            'taux_horaire', 'date_creation'
        ]
        read_only_fields = ['id', 'date_creation', 'full_name', 'department_nom']

    def get_full_name(self, obj):
        return obj.get_full_name()