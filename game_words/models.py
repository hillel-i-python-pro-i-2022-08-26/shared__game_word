from django.core.exceptions import ValidationError
from django.db import models


class Room(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.created_at}"

    __repr__ = __str__


class Word(models.Model):
    word = models.CharField(max_length=100)

    room = models.ForeignKey(
        Room,
        related_name="words",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "room",
                    "word",
                ],
                name="unique_word_per_room",
                violation_error_message="Unique word must be provided",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.room}: {self.word}"

    __repr__ = __str__

    def clean(self):
        self.word = self.word.strip()

        if not self.word:
            raise ValidationError("Word is required.")
        elif len(self.word.split()) > 1:
            raise ValidationError("Must be only 1 word")
        elif not self.word.isalpha():
            raise ValidationError("Bad characters.")

        last_word = self.room.words.order_by("-created_at").first()
        if (last_word is not None) and (required_character := last_word.word[-1].lower()) != self.word[0].lower():
            raise ValidationError(f'Bad word. Must started with "{required_character}"')
