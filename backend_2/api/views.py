from django.db.models import Sum
from django.http import FileResponse
from receipt.models import (FavoritesReceipt, Ingredient, IngredientReceipt,
                            Receipt, ShoppingList, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (FavoriteReceiptSerializers, IngredientSerializers,
                          ReceiptSerializers, TagSerializers, ReceiptCreateSerializers)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get',)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    permission_classes = (IsAuthenticated, )
    pagination_class = None


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    #serializer_class = ReceiptSerializers
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReceiptSerializers
        else:
            return ReceiptCreateSerializers

    #def perform_create(self, serializer):
        #serializer.save(author=self.request.user)
    

    @action(
        detail=True,
        url_path='favorite',
        methods=('post', 'delete'),
    )
    def favorite(self, request, pk):
        receipt = Receipt.objects.get(id=pk)
        favorite_recipe = FavoritesReceipt.objects.filter(
                user=request.user,
                receipt=receipt
            ).exists()

        if request.method == 'POST':
            if favorite_recipe:
                message = {
                    'errors': 'Рецепт уже есть в избранном'
                }
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                FavoritesReceipt.objects.create(
                    user=request.user,
                    receipt=receipt
                    )
                serialize = FavoriteReceiptSerializers(receipt)
                return Response(serialize.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if favorite_recipe:
                FavoritesReceipt.objects.get(
                    user=request.user,
                    receipt=receipt
                    ).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            message = {
                'errors': 'Рецепта нет в избранном'
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        url_path='shopping_cart',
        methods=('post', 'delete')
    )
    def shopping_cart(self, request, pk):
        receipt = Receipt.objects.get(id=pk)
        message = {
            'post': {'errors': 'Рецепт уже добавлен в список  покупок'},
            'del': {'errors': 'Рецепта нет в списке покупок'},
        }
        receip_in_sl = ShoppingList.objects.filter(
            receipt=receipt,
            user=self.request.user
            ).exists()

        if request.method == 'POST':
            if receip_in_sl:
                return Response(
                    message['post'],
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                ShoppingList.objects.create(
                    receipt=receipt,
                    user=self.request.user
                )
                serialize = FavoriteReceiptSerializers(receipt)
                return Response(serialize.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if receip_in_sl:
                ShoppingList.objects.get(
                    receipt=receipt,
                    user=self.request.user
                    ).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    message['del'],
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(
        detail=False,
        methods=('get',)
    )
    def download_shopping_cart(self, request):
        user = request.user
        sp = list(
            IngredientReceipt.objects.filter(
                receipt__sl_receipt__user=user).values(
                'ingredient__name',
                'ingredient__measurement_unit').annotate(
                ingredient_amount=Sum('amount')))
        data = []
        data.append('Список покупок \n')
        data.append('Ингридиент масса единица измерения \n')

        for el in sp:
            name = el['ingredient__name']
            msu = el['ingredient__measurement_unit']
            amount = el['ingredient_amount']
            data.append(f'{name}: {amount}.{msu} \n')
            print(f'{name}: {amount}.{msu}')

        return FileResponse(
            data,
            filename="shop_list.txt",
        )
