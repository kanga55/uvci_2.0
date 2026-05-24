from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display  = ['intitule', 'filiere', 'niveau', 'semestre', 'nombre_heures', 'credits']
    list_filter   = ['niveau', 'semestre', 'filiere']
    search_fields = ['intitule', 'filiere']