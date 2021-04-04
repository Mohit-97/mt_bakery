from rest_framework import generics, permissions
from order_management.models import Order
from order_management.serializers import  CreateOrderSerializer


class OrderView(generics.ListCreateAPIView, generics.GenericAPIView):
    """
    View for managing orders.
    """
    queryset = Order.objects.order_by('id')
    serializer_class = CreateOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(customer=self.request.user)

        return queryset
