from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    SmoothieCreateSerializer,
    SmoothieSerializer,
    SmoothieUpdateSerializer,
)
from .services import SmoothieService


class SmoothieViewSet(ViewSet):
    # ================================================================= #
    # YOUR TASKS BELOW
    # Note: You are free to change the base class of this ViewSet
    # (e.g., to ModelViewSet, GenericViewSet with mixins) or keep
    # using the Service layer. Choose the approach you prefer!
    # ================================================================= #

    def get_service(self) -> SmoothieService:
        return SmoothieService()

    @extend_schema(
        request=SmoothieCreateSerializer, responses={201: SmoothieSerializer}
    )
    def create(self, request):
        service = self.get_service()
        smoothie = service.create_smoothie(request.data)
        return Response(
            SmoothieSerializer(smoothie).data, status=status.HTTP_201_CREATED
        )

    @extend_schema(responses={200: SmoothieSerializer})
    def retrieve(self, request, pk=None):
        service = self.get_service()
        smoothie = service.get_smoothie_by_id(pk)
        if not smoothie:
            return Response(
                {"detail": "Smoothie not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(SmoothieSerializer(smoothie).data)

    @extend_schema(
        request=SmoothieUpdateSerializer, responses={200: SmoothieSerializer}
    )
    def partial_update(self, request, pk=None):
        service = self.get_service()
        smoothie = service.update_smoothie(pk, request.data)
        if not smoothie:
            return Response(
                {"detail": "Smoothie not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(SmoothieSerializer(smoothie).data)

    # TODO Task 1: GET /api/smoothies/

    # TODO Task 2: DELETE /api/smoothies/{id}/

    # TODO Task 3: GET /api/smoothies/{id}/nutrition/

    # Task 4: Generate random smoothie (pre-implemented)
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
        service = self.get_service()
        smoothie = service.generate_random_smoothie(count)
        return Response(
            SmoothieSerializer(smoothie).data, status=status.HTTP_201_CREATED
        )
