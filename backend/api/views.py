from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from receipt.models import (FavoritesReceipt, Ingredient, IngredientReceipt,
                            Receipt, ShoppingList, Tag)
from .filters import IngredientFilter, ReceiptFilter
from .functions import favoritе_or_shopping_cart
from .permissions import IsAuthorOrRedOnly
from .serializers import (IngredientSerializers, ReceiptCreateSerialize,
                          ReceiptSerializers, TagSerializers)


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
    permission_classes = (IsAuthorOrRedOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ReceiptFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReceiptSerializers
        return ReceiptCreateSerialize

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        url_path='favorite',
        methods=('post', 'delete'),
    )
    def favorite(self, request, pk):
        return favoritе_or_shopping_cart(
            request,
            pk,
            FavoritesReceipt,
        )

    @action(
        detail=True,
        url_path='shopping_cart',
        methods=('post', 'delete')
    )
    def shopping_cart(self, request, pk):
        return favoritе_or_shopping_cart(
            request,
            pk,
            ShoppingList,
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
                receipt__shoppinglist_receipt__user=user).values(
                'ingredient__name',
                'ingredient__measurement_unit').annotate(
                ingredient_amount=Sum('amount')))

        data = ''
        data += 'Список покупок \n'
        data += 'Ингредиент масса единица измерения \n'

        for number, element in enumerate(shoping_list):
            name = element['ingredient__name']
            msu = element['ingredient__measurement_unit']
            amount = element['ingredient_amount']
            data += f'{number+1}. {name} {amount} {msu}. \n'

        response = HttpResponse(
            data,
            content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = 'attachment; filename=shop_list'
        return response
