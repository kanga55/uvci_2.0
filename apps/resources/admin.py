from django.contrib import admin
from .models import Sequence, Resource


@admin.register(Sequence)
class SequenceAdmin(admin.ModelAdmin):
    list_display  = ['cours', 'ordre', 'titre']
    list_filter   = ['cours']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display  = ['titre', 'type_ressource', 'complexite', 'enseignant', 'sequence', 'date_creation']
    list_filter   = ['type_ressource', 'complexite']
    search_fields = ['titre']