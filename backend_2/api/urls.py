from django.urls import path, include

from user.views import get_token, TokenDestroy, UserViewSet

from rest_framework.routers import SimpleRouter 

from .views import TagViewSet, IngredientViewSet, Pusto


router_api = SimpleRouter()
#router_api.register('tags', TagViewSet)
router_api.register('users', UserViewSet)
router_api.register('tags', TagViewSet)
router_api.register('ingredients', IngredientViewSet)

router_api.register('pusto', Pusto, basename='pusto')



urlpatterns = [
    path('', include(router_api.urls)),
    
    #path('', include('djoser.urls')),
    #path('', include('djoser.urls.authtoken')),
    #path('', include('djoser.urls.jwt')),

    # получить токен авторизации
    path('auth/token/login/', get_token, name='login'),
    # удаление токена
    path('auth/token/logout/', TokenDestroy.as_view())

]




