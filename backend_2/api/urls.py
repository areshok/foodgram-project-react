from django.urls import path, include

from user.views import get_token


import djoser.urls.authtoken

urlpatterns = [
    
    
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    #path('', include('djoser.urls.jwt')),
    path('auth1/token/login/', get_token, name='login')

]




