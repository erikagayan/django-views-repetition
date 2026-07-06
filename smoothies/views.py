import random

import requests
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView

from .models import Ingredient, Smoothie
from .serializers import (
    SmoothieCreateSerializer,
    SmoothieSerializer,
    SmoothieUpdateSerializer,
)

FRUITYVICE_ALL_URL = "https://www.fruityvice.com/api/fruit/all"


class SmoothieAPIView(APIView):
    def get(self, request):
        total = Smoothie.objects.count()
        draft = Smoothie.objects.filter(status="DRAFT").count()
        published = Smoothie.objects.filter(status="PUBLISHED").count()

        return Response({"total": total, "draft": draft, "published": published}, status=HTTP_200_OK)


class SmoothieViewSet(ViewSet):
    # ================================================================= #
    # YOUR TASKS BELOW
    # ================================================================= #

    @extend_schema(
        request=SmoothieCreateSerializer, responses={201: SmoothieSerializer}
    )
    def create(self, request):
        serializer = SmoothieCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        smoothie = serializer.save()
        return Response(
            SmoothieSerializer(smoothie).data, status=status.HTTP_201_CREATED
        )

    @extend_schema(responses={200: SmoothieSerializer})
    def retrieve(self, request, pk=None):
        try:
            smoothie = Smoothie.objects.prefetch_related("ingredients").get(pk=pk)
        except Smoothie.DoesNotExist:
            return Response(
                {"detail": "Smoothie not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(SmoothieSerializer(smoothie).data)

    @extend_schema(
        request=SmoothieUpdateSerializer, responses={200: SmoothieSerializer}
    )
    def partial_update(self, request, pk=None):
        try:
            smoothie = Smoothie.objects.get(pk=pk)
        except Smoothie.DoesNotExist:
            return Response(
                {"detail": "Smoothie not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = SmoothieUpdateSerializer(
            smoothie, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(SmoothieSerializer(smoothie).data)

    # TODO Task 1: GET /api/smoothies/

    # TODO Task 2: DELETE /api/smoothies/{id}/

    # TODO Task 3: GET /api/smoothies/{id}/nutrition/

    # Task 4: Generate random smoothie (pre-implemented, contains bugs)
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="count",
                description="Number of random fruits (1-10)",
                required=False,
                type=int,
            ),
        ],
        responses={201: SmoothieSerializer},
    )
    @action(detail=False, methods=["post"], url_path="generate")
    def generate(self, request):
        count = int(request.query_params.get("count", 3))
        if count < 1 or count > 10:
            return Response(
                {"detail": "Count must be between 1 and 10."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = requests.get(FRUITYVICE_ALL_URL)
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

        return Response(
            SmoothieSerializer(smoothie).data, status=status.HTTP_201_CREATED
        )
