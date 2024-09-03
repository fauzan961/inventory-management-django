from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['patch'], url_path='remove-quantity/(?P<product_id>\d+)')
    def remove_quantity(self, request, product_id=None):
        product = get_object_or_404(Product, pk=product_id)
        quantity_sold = request.data.get('quantity_sold')

        try:
            quantity_sold = int(quantity_sold)
        except (TypeError, ValueError):
            return Response({'error': 'Invalid or missing quantity_sold'}, status=status.HTTP_400_BAD_REQUEST)

        if quantity_sold is not None:
            if product.quantity >= quantity_sold:
                product.quantity -= quantity_sold
                product.save()
                return Response({'message': 'Quantity updated successfully', 'remaining_quantity': product.quantity})
            else:
                return Response({'error': 'Insufficient quantity available'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Quantity_sold cannot be null'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['patch'], url_path='add-quantity/(?P<product_id>\d+)')
    def add_quantity(self, request, product_id=None):
        product = get_object_or_404(Product, pk=product_id)
        quantity_added = request.data.get('quantity_added')

        try:
            quantity_added = int(quantity_added)
        except (TypeError, ValueError):
            return Response({'error': 'Invalid or missing quantity_added'}, status=status.HTTP_400_BAD_REQUEST)

        if quantity_added is not None:
            product.quantity += quantity_added
            product.save()
            return Response({'message': 'Quantity updated successfully', 'remaining_quantity': product.quantity})
        else:
            return Response({'error': 'Quantity_added cannot be null'}, status=status.HTTP_400_BAD_REQUEST)
