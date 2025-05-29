from django.urls import path, include
from .views import (
    home_view,
    login_view,
    register_view,
    token_generator_view,
    logout_view,
)

app_name = "frontend"

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("token-generator/", token_generator_view, name="token_generator"),
    path("schema-viewer/", include("schema_viewer.urls")),
]
