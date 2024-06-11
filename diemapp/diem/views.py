from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from .models import *
from diem import serializers, paginators
from rest_framework.decorators import action


# Create your views here.
class ActivityViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    pagination_class = paginators.ActivityPaginator

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(name__icontains=q)

        return queries

    # def list(self, request, *args, **kwargs):
    #     return Response(serializers.ActivitySerializer(self.get_queryset(), many=True).data)


class TrainingPointViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView,generics.CreateAPIView):
    queryset = TrainingPoint.objects.filter(active=True).all()
    serializer_class = serializers.TrainingPointSerializer
    pagination_class = paginators.ScorePaginator

    # def get


class StatuteViewSet(viewsets.ViewSet,generics.ListAPIView):
    queryset = Statute.objects.all()
    serializer_class = serializers.StatuteSerializer


class StudentViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer

    @action(methods=['get'], detail=True)
    def activity(self, request, pk):
        activity = self.get_object().activity.all()

        return Response(serializers.ActivitySerializer(activity, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def registration(self, request, pk):
        student = self.get_object()
        registrations = Registration.objects.filter(student=student)
        return Response(serializers.RegistrationSerializer(registrations, many=True).data, status=status.HTTP_200_OK)


class MissingPointsReportViewSet(viewsets.ViewSet,generics.ListAPIView, generics.RetrieveAPIView):
    queryset = MissingPointsReport.objects.all()
    serializer_class = serializers.MissingPointsReportSerializer

    @action(methods=['patch'], url_path='approved', detail=True)
    def update_approved(self, request, pk):
        report = self.get_object()
        status_value = request.data.get('approved')
        report.approved = status_value
        report.save()
        return Response(serializers.MissingPointsReportSerializer(report).data, status=status.HTTP_200_OK)
