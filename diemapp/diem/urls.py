from django.urls import path, re_path, include
from rest_framework import routers
from diem import views


router = routers.DefaultRouter()
router.register('activities', views.ActivityViewSet, basename='activities')

urlpatterns = [
    path('', include(router.urls))

]
