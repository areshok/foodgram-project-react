from django.urls import path, include

from rest_framework.routers import DefaultRouter

import user.views

router_api = DefaultRouter()
#router_api.register('token', user.views.get_token, basename='token')

urlpatterns = [
    path('', include(router_api.urls)),

    path('token/',user.views.get_token, name='token' ),
]
    


