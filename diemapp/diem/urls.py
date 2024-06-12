from django.urls import path, re_path, include
from rest_framework import routers
from diem import views


router = routers.DefaultRouter()
router.register('activities', views.ActivityViewSet, basename='activities')
router.register('trainingPoints', views.TrainingPointViewSet, basename='trainingPoints')
router.register('statutes', views.StatuteViewSet, basename='statute')
router.register('students', views.StudentViewSet, basename='student')
router.register('missing-report', views.MissingPointsReportViewSet, basename='missing-report')
router.register('users', views.UserViewSet, basename='users')
router.register('comment', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls))

]
