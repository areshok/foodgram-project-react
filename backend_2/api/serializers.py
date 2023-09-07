from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField


from receipt.models import Tag, Ingredient, Receipt, IngredientReceipt

from user.serializers import UserSerializers


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class IngredientDetailSerializer(serializers.ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')    
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientReceipt
        fields = ["id", "name", "measurement_unit", "amount"]


class ReceiptSerializers(serializers.ModelSerializer):
    tags = TagSerializers(read_only=True, many=True)
    author = UserSerializers()
    ingredients = IngredientDetailSerializer(source="ingredientreceipt_set", many=True)

    class Meta:
        model = Receipt
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  #
                  #
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  )
        


class FavoriteReceiptSerializers(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class ShoppingListSerializers(serializers.ModelSerializer):
    ingredients = IngredientDetailSerializer(source="ingredientreceipt_set", many=True)
    class Meta:
        model = Receipt
        fields = ('ingredients',)