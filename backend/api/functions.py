from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from receipt.models import Receipt
from .serializers import FavoriteReceiptSerializers


def favoritе_or_shopping_cart(request, pk, model):
    message = {
        'post': {'errors': 'Рецепт уже добавлен в список'},
        'del': {'errors': 'Рецепта нет в списке'},
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
        model.objects.create(
            user=request.user,
            receipt=receipt
        )
        serialize = FavoriteReceiptSerializers(receipt)
        return Response(serialize.data, status=status.HTTP_201_CREATED)

    if check_receipt:
        get_object_or_404(
            model,
            user=request.user,
            receipt=receipt
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(message['del'], status=status.HTTP_400_BAD_REQUEST)
