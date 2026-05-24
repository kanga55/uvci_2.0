from django.urls import path
from . import views

urlpatterns = [
    path('annees/',  views.AnneeAcademiqueListView.as_view(), name='annees'),
    path('',         views.ActivityListCreateView.as_view(),  name='activities'),
    path('volume/',  views.VolumeHoraireView.as_view(),       name='volume-horaire'),
]