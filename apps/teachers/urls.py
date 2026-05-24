from django.urls import path
from . import views

urlpatterns = [
    path('departments/',     views.DepartmentListView.as_view(),    name='departments'),
    path('',                 views.TeacherListCreateView.as_view(), name='teachers'),
    path('<int:pk>/',        views.TeacherDetailView.as_view(),     name='teacher-detail'),
]