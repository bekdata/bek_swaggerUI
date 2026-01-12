from django.shortcuts import render
# swagger/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializers

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Faqat foydalanuvchining o'z mahsulotlarini qaytaradi
        return Product.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Yaratayotganda joriy foydalanuvchini egasi sifatida belgilaydi
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_expensive(self, request, pk=None):
        product = self.get_object()
        product.price += 100
        product.save()
        return Response({'status': 'Price increased', 'new_price': product.price})