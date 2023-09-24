from receipt.models import (FavoritesReceipt, Ingredient, IngredientReceipt,
                            Receipt, ShoppingList, Tag, TagReceipt)
from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from user.serializers import UserSerializers

from .fields import Base64ImageField


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
        read_only=True,
        many=True,
        source="ir_receipt",
    )
    is_favorited = serializers.SerializerMethodField(
        required=False,
        read_only=True,
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        required=False,
        read_only=True,
    )
    image = Base64ImageField()

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

    def create(self, validated_data):
        receipt = Receipt.objects.create(**validated_data)
        self.create_tag(receipt)
        self.create_ingridients(receipt)
        return receipt

    def validate_ingredients(self, value):
        if value is None:
            raise serializers.ValidationError('нет интгридиентов')
        if len(value) == 0:
            raise serializers.ValidationError('нет интгридиентов')
        for element in value:
            if type(element['id']) is not int:
                raise serializers.ValidationError('Не целочисленное число')
            if type(element['amount']) is not int:
                raise serializers.ValidationError('Не целочисленное число')
        id_list = []
        for element in value:
            id_list.append(element['id'])
        if len(id_list) > len(set(id_list)):
            raise serializers.ValidationError('Содержит дубликаты')
        return value

    def validate_tags(self, value):
        if value is None:
            raise serializers.ValidationError('нет тегов')
        for element in value:
            if type(element) is not int:
                raise serializers.ValidationError('Не целочисленное число')
        if len(value) > len(set(value)):
            raise serializers.ValidationError('Содержит дубликаты')
        return value

    def create_ingredients(self, receipt):
        ingridients = self.validated_data.get('ingredients')
        objs = []
        for element in ingridients:
            ingredient = Ingredient.objects.get(id=element['id'])
            amount = element['amount']
            objs.append(IngredientReceipt(
                receipt=receipt,
                ingredient=ingredient,
                amount=amount)
            )
        IngredientReceipt.objects.bulk_create(objs)

    def create_tag(self, receipt):
        tags = self.validated_data.get('tags')
        objs = []
        for tag in tags:
            curent_tag = Tag.objects.get(id=tag)
            objs.append(TagReceipt(tag=curent_tag, receipt=receipt))
        TagReceipt.objects.bulk_create(objs)

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        instance.t_receipt.all().delete()
        self.create_tag(instance)
        instance.ir_receipt.all().delete()
        self.create_ingridients(instance)
        return super().update(instance, validated_data)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return (
                FavoritesReceipt.objects.filter(
                    user=request.user, receipt=obj
                ).exists())
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return (
                ShoppingList.objects.filter(
                    user=request.user, receipt=obj
                ).exists())
        return False


class ReceiptSubscribeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
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
    ingredients = IngredientDetailSerializer(
        source="ingredientreceipt_set",
        many=True
    )

    class Meta:
        model = Receipt
        fields = ('ingredients',)
