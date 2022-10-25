from django.urls import path

from . import views

app_name = "game_words"

urlpatterns = [
    path("", views.index, name="index"),
    path("new-room", views.create_new_room, name="new_room"),
    path("room/<int:pk>", views.handle_room, name="room"),
]
