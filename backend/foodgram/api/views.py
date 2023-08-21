from django.shortcuts import render
from rest_framework import viewsets

from rest_framework import mixins

from .serializers import TagSerializers, RecipeSerializers

from recipes.models import Tag, Recipe

from rest_framework import permissions



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    permission_classes = [permissions.IsAuthenticated, ]
    http_method_names = ['get']



class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializers




