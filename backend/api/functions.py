from django.shortcuts import get_object_or_404
from receipt.models import Receipt
from rest_framework import status
from rest_framework.response import Response

from .serializers import FavoriteReceiptSerializers


def favorit_or_shopping_cart(request, pk, model, name_functions):
    what_function = {
        'favorite': 'избранное',
        'shopping_cart': 'список покупок'
    }

    message = {
        'post': {'errors': ('Рецепт уже добавлен в'
                            f'{what_function[name_functions]}')},
        'del': {'errors': f'Рецепта нет в {what_function[name_functions]}'},
    }
    receipt = get_object_or_404(Receipt, id=pk)
    check_receipt = model.objects.filter(
        user=request.user,
        receipt=receipt
    ).exists()

    if request.method == 'POST':
        if check_receipt:
            return Response(
                message['post'],
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            model.objects.create(
                user=request.user,
                receipt=receipt
            )
            serialize = FavoriteReceiptSerializers(receipt)
            return Response(serialize.data, status=status.HTTP_201_CREATED)

    if check_receipt:
        model.objects.get(
            user=request.user,
            receipt=receipt
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(message['del'], status=status.HTTP_400_BAD_REQUEST)
