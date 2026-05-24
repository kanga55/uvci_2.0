from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/teachers/', include('apps.teachers.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/resources/', include('apps.resources.urls')),
    path('api/activities/', include('apps.activities.urls')),
    path('api/reports/', include('apps.reports.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)