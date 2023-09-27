from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from user.serializers import UserSerializers
from receipt.models import (FavoritesReceipt, Ingredient, IngredientReceipt,
                            Receipt, ShoppingList, Tag, TagReceipt)
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
        source="ingredientreceipt_receipt",
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


class IngredientReceiptCreate(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def to_internal_value(self, data):
        id = data.get('id')
        amount = data.get('amount')
        return {
            'id': id,
            'amount': amount
        }


class ReceiptCreateSerialize(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientReceiptCreate(
        write_only=True,
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    author = UserSerializers(required=False)

    class Meta:
        model = Receipt
        fields = (
            'name',
            'text',
            'cooking_time',
            'author',
            'image',
            'ingredients',
            'tags',
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        receipt = Receipt.objects.create(**validated_data)
        self.create_tag(receipt, tags)
        self.create_ingredients(receipt, ingredients)
        return receipt

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        super().update(instance, validated_data)
        instance.tagreceipt_receipt.all().delete()
        self.create_tag(instance, tags)
        instance.ingredientreceipt_receipt.all().delete()
        self.create_ingredients(instance, ingredients)
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        return ReceiptSerializers(
            instance,
            context={'request': request}
        ).data

    def create_tag(self, receipt, tags):
        objs = []
        for tag in tags:
            objs.append(TagReceipt(tag=tag, receipt=receipt))
        TagReceipt.objects.bulk_create(objs)

    def create_ingredients(self, receipt, ingredients):
        objs = []
        for element in ingredients:
            objs.append(IngredientReceipt(
                receipt=receipt,
                ingredient_id=element['id'],
                amount=element['amount'])
            )
        IngredientReceipt.objects.bulk_create(objs)

    def validate_tags(self, value):
        tags_id = []
        for element in value:
            tags_id.append(element.id)
        if len(tags_id) > len(set(tags_id)):
            raise serializers.ValidationError('дубликаты тегов')
        return value

    def validate_ingredients(self, value):
        for element in value:
            if not element['id'].isdigit():
                raise serializers.ValidationError(
                    ' id не целочисленное число'
                )
            if not element['amount'].isdigit():
                raise serializers.ValidationError(
                    'amount не целочисленное число'
                )
        id_list = []
        for element in value:
            id_list.append(element['id'])
        if len(id_list) > len(set(id_list)):
            raise serializers.ValidationError(
                'Содержит дубликаты ингредиентов'
            )

        return value


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
