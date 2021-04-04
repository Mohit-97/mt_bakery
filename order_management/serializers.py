from django.db.models import Sum

from rest_framework import serializers

from order_management.models import Order, OrderItem
from product.serializers import ProductSerializer, IngredientsSerializer
from product.models import Product


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('quantity', 'product')


class CreateOrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, write_only=True)
    product_details = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'products', 'product_details',
                    'total_price', 'order_date']


    def validate(self, attrs):
        request = self.context.get('request')
        if request.user.is_staff:
            msg = "Only Customers are allowed to make orders for now."
            raise serializers.ValidationError(msg)

        attrs.update({'customer': request.user})
        return attrs

    def validate_products(self, products):

        for product in products:
            product_obj = product['product']
            available_quantity = product_obj.available_quantity
            quantity_to_buy = product['quantity']
            product_name = product_obj.name

            if (available_quantity < quantity_to_buy):
                    error = "Only {} Products are available for {}".format(
                                available_quantity, product_name)
                    raise serializers.ValidationError(error)

            if not product_obj.is_active:
                error = "{} is not available.".format(product_name)
                raise serializers.ValidationError(error)


        return products

    def create(self, validated_data):
        products = validated_data.pop('products')
        instance = super().create(validated_data)

        order_list = list()
        for product in products:
            quantity = product['quantity']
            product_obj = product['product']

            #finding total price for a product
            ordered_price = (product_obj.selling_price) * quantity

            order_list.append(OrderItem(order=instance,
                                        product=product_obj,
                                        quantity=quantity,
                                        ordered_price=ordered_price
                                        )
                                    )
            product_obj.available_quantity = product_obj.available_quantity - quantity
            product_obj.save()

        OrderItem.objects.bulk_create(order_list)

        return instance

    def get_product_details(self, obj):
        return list(obj.order_items.values())

    def get_total_price(self, obj):
        #get the total price for all the products order
        return obj.order_items.all().aggregate(Sum('ordered_price')
                                                ).get('ordered_price__sum', 0)

    def get_customer_name(self, obj):
        if obj.customer:
            return "{} {}".format(
                        obj.customer.first_name,
                        obj.customer.last_name
                    )

        return "Anonymous"
