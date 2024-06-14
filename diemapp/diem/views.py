from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import permissions, viewsets, generics, status, parsers
from .models import *
from diem import serializers, paginators, perms
from rest_framework.decorators import action


# Create your views here.
class ActivityViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivityDetailSerializer
    pagination_class = paginators.ActivityPaginator

    # permission_classes = [permissions.AllowAny()]

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(name__icontains=q)

        return queries

    def get_permissions(self):
        if self.action in ['add_comment', 'join_activity', 'like']:
            return [perms.IsStudentAuthenticated()]
        if self.action in ['create']:
            return [perms.IsAssistantAuthenticated()]

        return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(methods=['post'], url_path='comment', detail=True)
    def add_comment(self, request, pk):
        user = request.user
        student = Student.objects.get(id=user.id)
        c = Comment.objects.create(student=student, activity=self.get_object(),
                                   content=request.data.get('content'))

        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='student')
    def join_activity(self, request, pk):
        user = request.user
        student = Student.objects.get(id=user.id)
        if Registration.objects.filter(student=student, activity=self.get_object()).exists():
            return Response({'error': 'Student already registered for this activity.'},
                            status=status.HTTP_400_BAD_REQUEST)
        registration = Registration.objects.create(student=student, activity=self.get_object(),
                                                   attended=request.data.get('attended'))

        return Response(serializers.RegistrationSerializer(registration).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='likes', detail=True)
    def like(self, request, pk):
        user = request.user
        student = Student.objects.get(id=user.id)
        like, created = Like.objects.get_or_create(student=student, activity=self.get_object())
        if not created:
            like.active = not like.active
            like.save()

        return Response(serializers.ActivityDetailSerializer(self.get_object(), context={'request': request}).data,
                        status=status.HTTP_200_OK)


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

    def get_permissions(self):
        if self.action in ['registration', 'get_trainingPoint', 'create_missing_point']:
            return [perms.IsStudentAuthenticated()]
        if self.action in ['achievements']:
            return [perms.IsAssistantAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=True)
    def registration(self, request, pk):
        student = self.get_object()
        registrations = Registration.objects.filter(student=student)
        return Response(serializers.RegistrationSerializer(registrations, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='trainingPoint')
    def get_trainingPoint(self, request, pk):
        student = self.get_object()
        trainingPoint = TrainingPoint.objects.filter(student=student)

        return Response(serializers.TrainingPointSerializer(trainingPoint, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='missing-point')
    def create_missing_point(self, request):
        user = request.user
        student = Student.objects.get(id=user.id)

        missing_report = MissingPointsReport.objects.create(student=student,
                                                            activity_id=request.data.get('activity_id'),
                                                            proof=request.data.get('proof'))

        return Response(serializers.CreateMissingPointsReportSerializer(missing_report).data,
                        status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=True, url_path="achievements")
    def achievements(self, request, pk):
        achievement = Achievements.objects.filter(student=self.get_object())
        return Response(serializers.AchievementSerializer(achievement, many=True).data, status=status.HTTP_200_OK)


class MissingPointsReportViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView,
                                 generics.DestroyAPIView):
    queryset = MissingPointsReport.objects.all()
    serializer_class = serializers.MissingPointsReportSerializer
    permission_classes = [perms.IsAssistantAuthenticated]

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


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.IsStudentOfAuthenticated]


class AssistantViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Assistant.objects.all()
    serializer_class = serializers.AssistantSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [perms.IsManagerAuthenticated()]
        return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        faculty = request.data.get('faculty')
        try:
            khoa = Faculty.objects.get(name=faculty)
        except Faculty.DoesNotExist:
            return Response({'error': 'Khoa not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data={
            'username': username,
            'email': email,
            'password': password,
            'faculty': khoa.id
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
