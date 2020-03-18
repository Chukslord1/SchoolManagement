from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "APP"
urlpatterns = [
    path("", views.index, name="index"),
    path("index.html", views.index, name="index"),
    path("auth-login.html", views.login, name="login"),
    path("pages-recoverpw-2.html", views.recover, name="recover"),
    path("auth-lock-screen.html", views.verify, name="verify"),





]
