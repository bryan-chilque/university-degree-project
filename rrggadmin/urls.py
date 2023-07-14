from django.urls import include, path

from . import views

seguro_vehicular_urlpatterns = (
    [
        path("lista/", views.SeguroVehicularListView.as_view(), name="list"),
        path("crear/", views.SeguroVehicularCreateView.as_view(), name="create"),
    ],
    "vehicular",
)

seguro_urlpatterns = (
    [
        path("vehicular/", include(seguro_vehicular_urlpatterns)),
    ],
    "seguro",
)

consultant_urlpatterns = (
    [
        path("list/", views.ConsultantListView.as_view(), name="list"),
        path("create/", views.ConsultantCreateView.as_view(), name="create"),
    ],
    "consultant",
)

app_name = "rrggadmin"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("seguro/", include(seguro_urlpatterns)),
    path("consultant/", include(consultant_urlpatterns)),
]
