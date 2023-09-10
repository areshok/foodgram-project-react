from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Sum
from .serializers import TagSerializers, IngredientSerializers, ReceiptSerializers, FavoriteReceiptSerializers, ShoppingListSerializers, IngredientDetailSerializer

from django.http import FileResponse

from receipt.models import Tag, Ingredient, Receipt, FavoritesReceipt, ShoppingList, IngredientReceipt

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
        #serializer_class = IngredientDetailSerializer
    )
    def download_shopping_cart(self, request):
        #queryset = ShoppingList.objects.filter(user=request.user)
        # User.objects.filter(sp_users__user=self.request.user) 

        user = request.user
        #sp = ShoppingList.objects.filter(user=user)
        sp = Ingredient.objects.filter(ir_ingridient__receipt__sl_receipt__user=user)
        sp = IngredientReceipt.objects.filter(receipt__sl_receipt__user=user)
        sp = list(IngredientReceipt.objects.filter(receipt__sl_receipt__user=user).values('ingredient__name', 'ingredient__measurement_unit').annotate(ingredient_amount=Sum('amount')))


        data = []
        data.append('Список покупок \n')
        data.append('Ингридиент масса единица измерения \n')

        for el in sp:
            name = el['ingredient__name']
            msu = el['ingredient__measurement_unit']
            amount = el['ingredient_amount']
            data.append(f'{name}: {amount}.{msu} \n')
            print(f'{name}: {amount}.{msu}')

        #IngredientReceipt.objects.filter(sl_receipt__user=user)
        #serialize = IngredientDetailSerializer(sp, many=True)
        #serialize = ReceiptSerializers(sp, many=True)
        return FileResponse(data, 
                        filename="shop_list.txt", )
        #return Response()



        IngredientReceipt.objects.filter(receipt__sl_receipt__user=user).values('ingredient__name', 'ingredient__measurement_unit').annotate(ingredient_amount=Sum('amount'))

        '''
        queryset = User.objects.filter(sp_users__user=self.request.user)

        #User.objects.filter(sp_users__user=user)
        Receipt.objects.filter(receipts=User.objects.filter(sp_users__user=user))

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = UserSerializers(page, many=True)
            custom_data = serializer.data
            return Response(custom_data)
        
        # from user.models import User
        # from receipt.models import Tag, Ingredient, Receipt, FavoritesReceipt, ShoppingList
        # user = User.objects.get(id=1)
        #
        '''
        
        '''
        from itertools import chain
        user = User.objects.get(id=1)






        from django.http import JsonResponse

        
        #sl = ShoppingList.objects.filter(user=user)
        #sl = Receipt.objects.all()
        #sl.receipts.filter(user=user)

        user = User.objects.get(id=1)
        data = Receipt.objects.filter(receipts__user=user)
        Receipt.objects.filter(receipt__receipt_i__receipt_sp__user=user)
        Receipt.objects.filter(receipt_sp__ingridient_i__owner_list=user)
        Ingredient.objects.filter(receipt__receipt_i=1)
        #return JsonResponse(list(data), safe=False)
        '''
        '''
        x = Receipt.objects.all()
        x.sl_receipt.all()
        u = user.sl_user.all()
        
        z = IngredientReceipt.objects.all()
        z.sl_receipt.all()
        Ingredient.objects.filter(ir_ingridient__ingredientreceipt__ir_receipt__receipt__author=user)
        Ingredient.objects.filter(sl_receipt__receipt__ir_receipt__user=user)
        '''

        '''
        user = User.objects.get(id=1)
        ShoppingList.objects.filter(ir_receipt__receipt_id__user=user)

        Ingredient.objects.filter(ir_receipt__ingredient__sl_receipt__user__user)
        # ir_receipt__ingredient__sl_user__user__user

        x = user.sl_user.all()
        x.ir_receipt

        y = Ingredient.objects.filter(receipt__ir_ingridient__sl_receipt__user=user)
        y.sl_receipt.ir_ingridient

        c = Receipt.objects.get(id=1)
        c.ir_receipt.values()

        #IngredientSerializers(Receipt.objects.filter(receipts__user=user))
        #IngredientDetailSerializer(Receipt.objects.filter(receipts__user=user))
        # ShoppingList.objects.filter(receipts__)
        # Thing.objects.filter(field__in=Another_Thing.object.filter())
        #ShoppingList.objects.filter()

        '''

class Pusto(viewsets.ViewSet):
    pass


def test_list():
    pass



