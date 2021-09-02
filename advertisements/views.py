from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import ModelViewSet

from .filters import AdvertisementFilter
from .models import Advertisement
from .permission import IsAuthOrReadOnly
from .serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filterset_class = AdvertisementFilter

    def list(self, request, *args, **kwargs):
        if request.user.is_anonymous or request.user.is_authenticated:
            self.queryset = Advertisement.objects.filter(~Q(status='DRAFT'))
        elif request.user.is_superuser or request.user.is_stuff:
            self.queryset = Advertisement.objects.all()
        else:
            self.queryset = Advertisement.objects.filter(~Q(status='DRAFT') & Q(creator=request.user))
        return super().list(self, request, *args, **kwargs)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            permissions = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permissions = [IsAuthOrReadOnly]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]
