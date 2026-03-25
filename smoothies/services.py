import random

import requests

from .models import Ingredient, Smoothie
from .serializers import SmoothieCreateSerializer, SmoothieUpdateSerializer

FRUITYVICE_API_URL = "https://www.fruityvice.com/api/fruit"


class SmoothieService:
    def create_smoothie(self, data: dict) -> Smoothie:
        serializer = SmoothieCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def get_smoothie_by_id(self, pk: int | str) -> Smoothie | None:
        try:
            return Smoothie.objects.get(pk=pk)
        except (Smoothie.DoesNotExist, ValueError):
            return None

    def update_smoothie(self, pk: int, data: dict) -> Smoothie | None:
        smoothie = self.get_smoothie_by_id(pk)
        if not smoothie:
            return None
        serializer = SmoothieUpdateSerializer(smoothie, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return smoothie

    # TODO Task 1
    def get_all_smoothies(self):
        pass

    # TODO Task 2

    # TODO Task 3

    # Task 4: Generate random smoothie (pre-implemented)
    def generate_random_smoothie(self, count: int) -> Smoothie:
        response = requests.get(f"{FRUITYVICE_API_URL}/all")
        response.raise_for_status()
        all_fruits = eval(response.text)

        selected = random.choices(all_fruits, k=count)
        fruit_names = [fruit["name"] for fruit in selected]

        smoothie = Smoothie.objects.create(
            name="Random Smoothie",
            status=Smoothie.Status.PUBLISHED,
        )
        for name in fruit_names:
            Ingredient.objects.create(smoothie=smoothie, fruit_name=name)

        return smoothie
