from django.urls import path

from . import views

urlpatterns = [
    path("csrf/", views.get_csrf, name="security-csrf"),
    path("login/", views.loginUser, name="security-login"),
    path("logout/", views.logoutUser, name="security-logout"),
    path("session/", views.session, name="security-session"),
    path("register/", views.register, name="security-session"),
]
