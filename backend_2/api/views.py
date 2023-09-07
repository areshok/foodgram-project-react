from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from .serializers import TagSerializers, IngredientSerializers, ReceiptSerializers, FavoriteReceiptSerializers, ShoppingListSerializers


from receipt.models import Tag, Ingredient, Receipt, FavoritesReceipt, ShoppingList

from user.models import User
from user.serializers import UserSerializers

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get',)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    permission_classes = (IsAuthenticated, )


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializers
    permission_classes = (IsAuthenticated,)

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
            'post' : {'errors': 'Рецепт уже добавлен в список  покупок'},
            'del' : {'errors': 'Рецепта нет в списке покупок'},
        }
        receip_in_sl = ShoppingList.objects.filter(
            receipt=receipt,
            user=self.request.user
            ).exists()

        if request.method == 'POST':
            if receip_in_sl:
                return Response(message['post'], status=status.HTTP_400_BAD_REQUEST)
            else:
                ShoppingList.objects.create(receipt=receipt, user=self.request.user)
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
                return Response(message['del'], status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=('get',)
    )
    def download_shopping_cart(self, request):
        #queryset = ShoppingList.objects.filter(user=request.user)
        # User.objects.filter(sp_users__user=self.request.user) 
        queryset = User.objects.filter(sp_users__user=self.request.user)

        #User.objects.filter(sp_users__user=user)
        Receipt.objects.filter(receipts=User.objects.filter(sp_users__user=user))

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = UserSerializers(page, many=True)
            custom_data = serializer.data
            return Response(custom_data)



class Pusto(viewsets.ViewSet):
    pass
