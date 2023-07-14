from django.urls import path

from . import views

app_name = "rrggweb"


urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path(
        "seguro/vehicular/",
        views.SeguroVehicularView.as_view(),
        name="seguro_vehicular",
    ),
]
