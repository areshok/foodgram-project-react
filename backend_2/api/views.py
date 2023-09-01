from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated

from .serializers import TagSerializers, IngredientSerializers


from receipt.models import Tag, Ingredient


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get',)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    permission_classes = (IsAuthenticated, )





class Pusto(viewsets.ViewSet):
    pass
