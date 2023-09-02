from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated

from .serializers import TagSerializers, IngredientSerializers, ReceiptSerializers


from receipt.models import Tag, Ingredient, Receipt


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get',)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    permission_classes = (IsAuthenticated, )


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializers


class Pusto(viewsets.ViewSet):
    pass
