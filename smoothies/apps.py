from django.apps import AppConfig


class SmoothiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "smoothies"

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(_seed_data, sender=self)


def _seed_data(sender, **kwargs):
    from .models import Ingredient, Smoothie

    if Smoothie.objects.exists():
        return

    tropical = Smoothie.objects.create(name="Tropical Blast", status="DRAFT")
    Ingredient.objects.bulk_create(
        [
            Ingredient(smoothie=tropical, fruit_name="Banana"),
            Ingredient(smoothie=tropical, fruit_name="Mango"),
            Ingredient(smoothie=tropical, fruit_name="Pineapple"),
        ]
    )

    berry = Smoothie.objects.create(name="Berry Mix", status="PUBLISHED")
    Ingredient.objects.bulk_create(
        [
            Ingredient(smoothie=berry, fruit_name="Strawberry"),
            Ingredient(smoothie=berry, fruit_name="Blueberryrr"),
            Ingredient(smoothie=berry, fruit_name="Bananasa"),
        ]
    )

    green = Smoothie.objects.create(name="Green Power", status="DRAFT")
    Ingredient.objects.bulk_create(
        [
            Ingredient(smoothie=green, fruit_name="Kiwi"),
            Ingredient(smoothie=green, fruit_name="Apple"),
            Ingredient(smoothie=green, fruit_name="Mango"),
        ]
    )

    citrus = Smoothie.objects.create(name="Citrus Burst", status="PUBLISHED")
    Ingredient.objects.bulk_create(
        [
            Ingredient(smoothie=citrus, fruit_name="Orange"),
            Ingredient(smoothie=citrus, fruit_name="Lemon"),
            Ingredient(smoothie=citrus, fruit_name="Lime"),
        ]
    )

    banana_boost = Smoothie.objects.create(name="Banana Boost", status="DRAFT")
    Ingredient.objects.bulk_create(
        [
            Ingredient(smoothie=banana_boost, fruit_name="Banana"),
            Ingredient(smoothie=banana_boost, fruit_name="Strawberry"),
            Ingredient(smoothie=banana_boost, fruit_name="Raspberry"),
        ]
    )

    sunset = Smoothie.objects.create(name="Mango Sunset", status="PUBLISHED")
    Ingredient.objects.bulk_create(
        [
            Ingredient(smoothie=sunset, fruit_name="Mango"),
            Ingredient(smoothie=sunset, fruit_name="Peach"),
            Ingredient(smoothie=sunset, fruit_name="Passion-Fruit"),
        ]
    )
