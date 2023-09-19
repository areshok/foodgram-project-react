
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from user.views import TokenViewSet, UserViewSet

from .views import IngredientViewSet, ReceiptViewSet, TagViewSet

router_api = SimpleRouter()
router_api.register('auth/token', TokenViewSet, basename='token')

router_api.register('users', UserViewSet)
router_api.register('tags', TagViewSet)
router_api.register('ingredients', IngredientViewSet)
router_api.register('recipes', ReceiptViewSet)

urlpatterns = [
    path('', include(router_api.urls)),
]
