from django.urls import path
from . import views

urlpatterns = [
    path('',          views.ReportListView.as_view(),     name='reports'),
    path('generate/', views.GenerateReportView.as_view(), name='generate-report'),
]