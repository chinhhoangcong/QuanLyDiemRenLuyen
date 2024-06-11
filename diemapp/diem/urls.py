from django.urls import path, re_path, include
from rest_framework import routers
from diem import views


router = routers.DefaultRouter()
router.register('activities', views.ActivityViewSet, basename='Hoạt Động Ngoại Khóa')
router.register('trainingPoints', views.TrainingPointViewSet, basename='Bảng Điểm Rèn Luyện')
router.register('statutes', views.StatuteViewSet, basename='statute')
router.register('students', views.StudentViewSet, basename='student')
router.register('missing-report', views.MissingPointsReportViewSet, basename='missing_report')
urlpatterns = [
    path('', include(router.urls))

]
