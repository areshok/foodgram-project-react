
from django.urls import path, include



from rest_framework.routers import SimpleRouter 

from .views import TagViewSet, IngredientViewSet, ReceiptViewSet, Pusto


from user.views import UserViewSet, TokenViewSet


router_api = SimpleRouter()
router_api.register('auth/token', TokenViewSet, basename='token')

router_api.register('users', UserViewSet)
router_api.register('tags', TagViewSet)
router_api.register('ingredients', IngredientViewSet)
router_api.register('recipes', ReceiptViewSet)







router_api.register('pusto', Pusto, basename='pusto')



urlpatterns = [
    path('', include(router_api.urls)),
]
