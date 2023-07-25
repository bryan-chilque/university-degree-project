from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="rrggweb:login")),
    path("accounts/login/", RedirectView.as_view(url="/")),
    path("web/", include("rrggweb.urls")),
    path("admin/", include("rrggadmin.urls")),
    path("_/", admin.site.urls),
]