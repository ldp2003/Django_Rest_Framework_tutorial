"""
URL configuration for tutorial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from tutorial.quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'products', views.ProductViewSet) 
# router.register(r'generic', views.UserList) #không được
# router.register(r'hello', views.hello_world, basename='hello_world') functional không phải viewset class nên như này ko đc

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('hello/', views.hello_world, name='hello_world'), 
    path('generic/', views.UserList.as_view(), name='user_list'), #chưa rõ generic để làm gì
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('template/', views.testing_templaterenderer, name='testing_templaterenderer'),
]