
from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authtoken_views
from database import views

## Create a router and register viewsets

router = DefaultRouter()

router.register(r'Source', views.SourceViewSet,basename='Source')
router.register(r'Result', views.ResultViewSet,basename='Result')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^api-token-auth/', authtoken_views.obtain_auth_token),
    url(r'api-auth/', include('rest_framework.urls')),
    url('^', include('django.contrib.auth.urls'))
]

