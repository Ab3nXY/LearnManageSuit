from django.contrib import admin
from django.urls import path, include
from .views import DashboardView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from  django.views.static import serve

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("calendar/", include("calendarapp.urls")),
    path('accounts/', include('allauth.urls')),
    # path("__debug__/", include("debug_toolbar.urls")),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

# Serve static and media files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
