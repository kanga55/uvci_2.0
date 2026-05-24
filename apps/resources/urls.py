from django.urls import path
from . import views

urlpatterns = [
    path('sequences/',        views.SequenceListCreateView.as_view(), name='sequences'),
    path('',                  views.ResourceListCreateView.as_view(), name='resources'),
    path('<int:pk>/',         views.ResourceDetailView.as_view(),     name='resource-detail'),
]