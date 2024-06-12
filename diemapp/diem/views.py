from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import permissions, viewsets, generics, status, parsers
from .models import *
from diem import serializers, paginators, perms
from rest_framework.decorators import action


# Create your views here.
class ActivityViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    pagination_class = paginators.ActivityPaginator
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(name__icontains=q)

        return queries

    def get_permissions(self):
        if self.action in ['add_comment']:
            return [permissions.IsAuthenticated()]

        return self.permission_classes

    @action(methods=['post'], url_path='comment', detail=True)
    def add_comment(self, request, pk):
        user = request.user
        student = Student.objects.get(id=user.id)
        c = Comment.objects.create(student=student, activity=self.get_object(),
                                   content=request.data.get('content'))

        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)


class TrainingPointViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = TrainingPoint.objects.filter(active=True).all()
    serializer_class = serializers.TrainingPointSerializer
    pagination_class = paginators.ScorePaginator


class StatuteViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Statute.objects.all()
    serializer_class = serializers.StatuteSerializer


class StudentViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer

    @action(methods=['get'], detail=True)
    def registration(self, request, pk):
        student = self.get_object()
        registrations = Registration.objects.filter(student=student)
        return Response(serializers.RegistrationSerializer(registrations, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='trainingPoint')
    def def_trainingPoint(self, request, pk):
        student = self.get_object()
        trainingPoint = TrainingPoint.objects.filter(student=student)

        return Response(serializers.TrainingPointSerializer(trainingPoint, many=True).data, status=status.HTTP_200_OK)


class MissingPointsReportViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = MissingPointsReport.objects.all()
    serializer_class = serializers.MissingPointsReportSerializer

    def get_queryset(self):
        queries = self.queryset
        q = self.request.query_params.get("khoa")
        if q:
            queries = queries.filter(student__clas__faculty__name__icontains=q)

        return queries

    @action(methods=['patch'], url_path='approved', detail=True)
    def update_approved(self, request, pk):
        report = self.get_object()
        status_value = request.data.get('approved')
        report.approved = status_value
        report.save()
        return Response(serializers.MissingPointsReportSerializer(report).data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_name="current-user", url_path="current-user", detail=False)
    def current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.IsStudentOfAuthenticated]
