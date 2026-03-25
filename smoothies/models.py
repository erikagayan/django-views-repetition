from django.db import models


class Smoothie(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"

    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )

    def __str__(self):
        return f"{self.name} ({self.status})"


class Ingredient(models.Model):
    smoothie = models.ForeignKey(
        Smoothie,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ingredients",
    )
    fruit_name = models.CharField(max_length=255)

    def __str__(self):
        return self.fruit_name
