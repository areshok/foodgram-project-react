from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from receipt.models import (FavoritesReceipt, Ingredient, IngredientReceipt,
                            Receipt, ShoppingList, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientFilter, ReceiptFilter
from .functions import favorit_or_shopping_cart
from .permissions import IsAuthorOrRedOnly
from .serializers import (IngredientSerializers, ReceiptSerializers,
                          TagSerializers)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    http_method_names = ('get',)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    http_method_names = ('get',)
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ('^name', )


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializers
    permission_classes = (IsAuthorOrRedOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ReceiptFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        url_path='favorite',
        methods=('post', 'delete'),
    )
    def favorite(self, request, pk):
        return favorit_or_shopping_cart(
            request,
            pk,
            FavoritesReceipt,
            'favorite',
        )

    @action(
        detail=True,
        url_path='shopping_cart',
        methods=('post', 'delete')
    )
    def shopping_cart(self, request, pk):
        return favorit_or_shopping_cart(
            request,
            pk,
            ShoppingList,
            'shopping_cart',
        )

    @action(
        detail=False,
        methods=('get',)
    )
    def download_shopping_cart(self, request):
        user = request.user

        if not ShoppingList.objects.filter(user=user).exists():
            return Response({'error': 'Список покупок пуст'},
                            status=status.HTTP_204_NO_CONTENT)

        shoping_list = list(
            IngredientReceipt.objects.filter(
                receipt__sl_receipt__user=user).values(
                'ingredient__name',
                'ingredient__measurement_unit').annotate(
                ingredient_amount=Sum('amount')))

        data = ''
        data += 'Список покупок \n'
        data += 'Ингридиент масса единица измерения \n'

        for n, el in enumerate(shoping_list):
            name = el['ingredient__name']
            msu = el['ingredient__measurement_unit']
            amount = el['ingredient_amount']
            data += f'{n+1}. {name} {amount} {msu}. \n'

        response = HttpResponse(
            data,
            content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = 'attachment; filename=shop_list'
        return response
