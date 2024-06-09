from rest_framework import viewsets, generics
from .models import *
from diem import serializers


# Create your views here.
class ActivityViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivitySerializer