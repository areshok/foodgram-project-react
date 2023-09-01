from rest_framework import serializers

from receipt.models import Tag, Ingredient, Receipt


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class ReceiptSerializers(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ('id',
                  #'tag',
                  #'author',
                  #'ingredient',
                  #
                  #
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  )