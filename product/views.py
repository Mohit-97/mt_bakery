from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.serializers import (ProductSerializer, IngredientsSerializer,
    InventoryUpdateSerializer)
from product.models import Product, Ingredients
from user.permissions import CustomPermission, CustomStrictPermission


class IngredientsViewSet(viewsets.ModelViewSet):

    permission_classes = (CustomStrictPermission,)
    queryset = Ingredients.objects.all().order_by('id')
    serializer_class = IngredientsSerializer


class ProductViewSet(viewsets.ModelViewSet):

    permission_classes = (CustomPermission,)
    queryset = Product.objects.all().order_by('-added_on')
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = super(ProductViewSet, self).get_queryset(*args, **kwargs)
        user = self.request.user

        if user.is_anonymous or not user.is_staff:
            queryset = queryset.filter(is_active=True, available_quantity__gt=0)

        return queryset

    @action(methods=['POST',], detail=True,
        serializer_class=InventoryUpdateSerializer)
    def update_inventory(self, request, *args, **kwargs):
        """
        ACTION ENUM:
        1 - ADD
        2 - REMOVE
        """
        serializer = self.get_serializer(data=request.data,
                        context={'request': request,
                            'product': self.get_object()})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)
