from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="rrggweb:login")),
    path("accounts/login/", RedirectView.as_view(url="/")),
    path("web/", include("rrggweb.urls")),
    path("admin/", include("rrggadmin.urls")),
    path("_/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]
