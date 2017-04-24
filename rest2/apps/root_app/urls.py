from django.conf.urls import url, include
from rest_framework import routers
from . import views

"""
instead of manually creating each RESTful route in our views.py, we can import rest_framework's routers, which will set all of that up for us in one line.
The first parameter is the prefix which will belong to this cluster of urls. The second parameter, the ViewSet, is the collection of methods which provide the functionality.

    router.register(r'users', views.UserViewSet)

The single line above is equivalent to the following:

    url(r'groups/$', views.index, name="index"),
    url(r'groups/(?P<id>)/$', views.show, name="detail")

"""
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

#here we include our router's urls
urlpatterns = [
    url(r'^', include(router.urls)),
]
