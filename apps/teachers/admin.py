from django.contrib import admin
from .models import Teacher, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['nom']
    search_fields = ['nom']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'prenom', 'grade', 'statut', 'department', 'taux_horaire']
    list_filter   = ['grade', 'statut', 'department']
    search_fields = ['nom', 'prenom', 'email']