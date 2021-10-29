from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>/", views.entry_page, name="entry"),
    path("search", views.search, name="search"),
    path("new_entry", views.new, name="new"),
    path("edit/<str:entry>/", views.edit_page, name="edit"),
    path("random", views.random, name="random")
]

