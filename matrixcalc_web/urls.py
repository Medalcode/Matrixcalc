from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from matrixcalc_web.views import spa_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("calculator.urls")),
]

# Catch-all for SPA routes (serves Vue frontend)
urlpatterns += [
    re_path(r"^(?!/?(api/|admin/|static/)).*$", spa_view, name="spa"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
