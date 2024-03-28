from django.contrib import admin
from django.urls import path, include
from .views import DashboardView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("calendarapp.urls")),
    path('accounts/', include('allauth.urls')),
    #path("__debug__/", include("debug_toolbar.urls")),
]

# Serve static and media files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
