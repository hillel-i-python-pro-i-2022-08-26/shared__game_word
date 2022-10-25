from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from . import models
from .forms import WordForm


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "game_words/index.html",
        {
            "title": "Room dispatcher",
        },
    )


def create_new_room(request: HttpRequest) -> HttpResponse:
    room = models.Room()
    room.save()

    return redirect("game_words:room", pk=room.pk)


def handle_room(request: HttpRequest, pk: int) -> HttpResponse:
    room = models.Room.objects.get(pk=pk)
    word = models.Word(room=room)

    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            form = WordForm(instance=word)

    else:
        form = WordForm(instance=word)

    words = room.words.order_by("-created_at").all()

    return render(
        request,
        "game_words/room.html",
        {
            "title": str(room),
            "form": form,
            "words": words,
        },
    )
