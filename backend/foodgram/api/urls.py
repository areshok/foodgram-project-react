from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TagViewSet, RecipeViewSet

from user.views import UserViewSet, get_token

router = DefaultRouter()

router.register('users', UserViewSet)

router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

from djoser.views import TokenDestroyView, TokenCreateView


urlpatterns = [
    path('', include(router.urls)),
    #path('auth/', include('djoser.urls'))

    path('auth/token/logout/', TokenDestroyView.as_view(), name="logout"),
    path('auth/token/login/', get_token, name="login")

]