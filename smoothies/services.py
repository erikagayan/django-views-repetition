import random
from concurrent.futures import ThreadPoolExecutor

import requests

from .clients import FruityviceClient
from .models import Ingredient, Smoothie
from .serializers import SmoothieCreateSerializer, SmoothieUpdateSerializer

FRUITYVICE_API_URL = "https://www.fruityvice.com/api/fruit"
NUTRITION_MAX_WORKERS = 8


class SmoothieService:
    def __init__(self, fruityvice_client: FruityviceClient | None = None) -> None:
        self._fruityvice_client = fruityvice_client or FruityviceClient()

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

    def get_smoothie_nutrition(self, pk: int | str) -> dict | None:
        """Aggregate calorie data for a smoothie's ingredients.

        Fruits unknown to Fruityvice (HTTP 404) are reported in
        ``skipped_fruits`` and excluded from the running total, per the
        task requirements.
        """
        smoothie = self.get_smoothie_by_id(pk)
        if smoothie is None:
            return None

        ingredients = list(smoothie.ingredients.all())
        fetched = self._fetch_fruits([i.fruit_name for i in ingredients])

        items: list[dict] = []
        skipped: list[str] = []
        total_calories = 0.0

        for fruit_name, payload in fetched:
            if payload is None:
                skipped.append(fruit_name)
                continue
            calories = float(payload.get("nutritions", {}).get("calories", 0) or 0)
            total_calories += calories
            items.append({"fruit_name": fruit_name, "calories": calories})

        return {
            "smoothie_id": smoothie.id,
            "name": smoothie.name,
            "total_calories": total_calories,
            "ingredients": items,
            "skipped_fruits": skipped,
        }

    def _fetch_fruits(self, fruit_names: list[str]) -> list[tuple[str, dict | None]]:
        """Fetch fruit payloads concurrently, preserving input order."""
        if not fruit_names:
            return []

        client = self._fruityvice_client
        workers = min(NUTRITION_MAX_WORKERS, len(fruit_names))
        with ThreadPoolExecutor(max_workers=workers) as executor:
            payloads = list(executor.map(client.get_fruit, fruit_names))
        return list(zip(fruit_names, payloads))

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
