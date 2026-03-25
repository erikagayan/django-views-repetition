from rest_framework import serializers

from .models import Ingredient, Smoothie


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "fruit_name"]


class SmoothieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smoothie
        fields = ["id", "name", "status"]


class SmoothieCreateSerializer(serializers.ModelSerializer):
    fruits = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        write_only=True,
        help_text="List of fruit names, must not be empty.",
    )

    class Meta:
        model = Smoothie
        fields = ["id", "name", "status", "fruits"]

    def create(self, validated_data):
        fruits = validated_data.pop("fruits")
        smoothie = Smoothie.objects.create(**validated_data)
        Ingredient.objects.bulk_create(
            [Ingredient(smoothie=smoothie, fruit_name=f) for f in fruits]
        )
        return smoothie


class SmoothieUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smoothie
        fields = ["name", "status"]
        extra_kwargs = {"name": {"required": False}, "status": {"required": False}}


# TODO Task 1
