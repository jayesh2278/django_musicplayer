from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "app"

urlpatterns = [
    path("a/", views.index, name="index"),
    path('<int:id>', views.coml, name="abcd"),
]
