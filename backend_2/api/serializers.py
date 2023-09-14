from receipt.models import (FavoritesReceipt, Ingredient, IngredientReceipt,
                            Receipt, ShoppingList, Tag, TagReceipt)
from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from user.serializers import UserSerializers


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientDetailSerializer(serializers.ModelSerializer):
    id = ReadOnlyField(
        source='ingredient.id'
    )
    name = ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = IngredientReceipt
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount"
        )


class ReceiptSerializers(serializers.ModelSerializer):
    tags = TagSerializers(
        read_only=True,
        many=True
    )
    author = UserSerializers(required=False)
    ingredients = IngredientDetailSerializer(
        source="ir_receipt",
        many=True
    )
    is_favorited = serializers.SerializerMethodField(
        required=False,
        read_only=True,
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        required=False,
        read_only=True,
    )

    class Meta:
        model = Receipt
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    '''
    def create(self, validated_data):
        print(validated_data)

        tags = validated_data.pop('tags')
        print(tags)
        receipt = Receipt.objects.create(*validated_data)
        for tag in tags:
            curent_tag, status = Tag.objects.get_or_create(tag)
            TagReceipt.objects.create(tag=curent_tag, receipt=receipt)
        return receipt
    '''


        ##return Receipt.objects.create(**validated_data)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (
            FavoritesReceipt.objects.filter(
                user=request.user, receipt=obj
            ).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (
            ShoppingList.objects.filter(
                user=request.user, receipt=obj
            ).exists())

'''
class IngridientRecetpCreate(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientReceipt
        fields = ('id', 'amount')
'''

class IngridientRecetpCreate(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()


        
class ReceiptCreateSerializers(serializers.ModelSerializer):
    author = UserSerializers(required=False)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    #ingredients = IngridientRecetpCreate(many=True, write_only=True)
    ingredients = IngredientDetailSerializer(
        source="ir_receipt",
        many=True
    )
    class Meta:
        model = Receipt
        fields = [
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        ]

    def create(self, validated_data):
        author = self.context['request'].user
        print(validated_data)
        tags = validated_data.pop('tags')
        #ingredients = validated_data.pop('ingredients')

        #print(ingredients[0])
        #for ingridient in ingredients:
            #print(ingridient['id'])

        receipt = Receipt.objects.create(author=author, **validated_data)
        for tag in tags:
            TagReceipt.objects.create(tag=tag, receipt=receipt)
        #for ingredient in ingredients:
            #IngredientReceipt.objects.create(ingredient=ingredient['id'], receipt=receipt, amount=ingredient['amount'] )
        return receipt

    '''
    def validate_ingredients(self, data):
        ingridients = []
        #print('validate_ingridients')
        for el in data:
            ingridient = el['id']
            amount = el['amount']
            ingridients.append((ingridient, amount))
            #print(f'{ingridient}  {amount}')
        return ingridients
    '''




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
    ingredients = IngredientDetailSerializer(
        source="ingredientreceipt_set",
        many=True
    )

    class Meta:
        model = Receipt
        fields = ('ingredients',)
