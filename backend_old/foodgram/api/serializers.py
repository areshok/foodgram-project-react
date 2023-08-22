from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from recipes.models import Tag, Recipe
from user.models import Follow

class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Recipe
        fields = ('id', 'tag', 'author', 'is_favorited', 'ingredient', 'name', 'image', 'text', 'cooking_time')

