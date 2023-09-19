import base64

from django.core.files.base import ContentFile
from receipt.models import (FavoritesReceipt, Ingredient, IngredientReceipt,
                            Receipt, ShoppingList, Tag, TagReceipt)
from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from user.serializers import UserSerializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


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

    def create_ingridients(self, receipt):
        ingridients = self.initial_data.get('ingredients')
        if ingridients is None:
            raise serializers.ValidationError(
                {'ingridients': 'нет интгридиентов'}
            )
        for element in ingridients:
            ingridient = Ingredient.objects.get(id=element['id'])
            amount = element['amount']
            IngredientReceipt.objects.create(
                receipt=receipt,
                ingredient=ingridient,
                amount=amount
            )

    def create_tag(self, receipt):
        tags = self.initial_data.get('tags')
        if tags is None:
            raise serializers.ValidationError({'tags': 'нет тегов'})
        tags = self.initial_data['tags']
        for tag in tags:
            curent_tag = Tag.objects.get(id=tag)
            TagReceipt.objects.create(tag=curent_tag, receipt=receipt)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        instance.t_receipt.all().delete()
        self.create_tag(instance)
        instance.ir_receipt.all().delete()
        self.create_ingridients(instance)
        return super().update(instance, validated_data)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if str(request.user) == 'AnonymousUser':
            return False
        else:
            return (
                FavoritesReceipt.objects.filter(
                    user=request.user, receipt=obj
                ).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if str(request.user) == 'AnonymousUser':
            return False
        else:
            return (
                ShoppingList.objects.filter(
                    user=request.user, receipt=obj
                ).exists())


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
