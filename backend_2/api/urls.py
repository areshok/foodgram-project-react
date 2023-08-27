from django.urls import path, include

from user.views import get_token, TokenDestroy


import djoser.urls.authtoken

urlpatterns = [
    
    
    path('', include('djoser.urls')),
    #path('', include('djoser.urls.authtoken')),
    #path('', include('djoser.urls.jwt')),
    path('auth/token/login/', get_token, name='login'),
    path('auth/token/logout/', TokenDestroy.as_view())

]




