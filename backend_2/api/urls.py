from django.urls import path, include

from user.views import get_token, TokenDestroy, UserViewSet

from rest_framework.routers import SimpleRouter 


router_api = SimpleRouter()
router_api.register('users', UserViewSet)
#router_api.register('set_password', PasswordChangeViewSet, basename='change_password')


import djoser.urls.authtoken
import djoser.urls

urlpatterns = [
    
    path('', include(router_api.urls)),
    
    #path('', include('djoser.urls')),
    #path('', include('djoser.urls.authtoken')),
    #path('', include('djoser.urls.jwt')),


    

    # список пользователей
    #path('users/', UserViewSet.as_view()),

    # получить токен авторизации
    path('auth/token/login/', get_token, name='login'),
    # удаление токена
    path('auth/token/logout/', TokenDestroy.as_view())

]




