from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    avatar = serializers.SerializerMethodField(source='avatar')

    def get_avatar(self, user):
        return user.avatar.url

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username'],
            role='assistant'
        )
        return user


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'active']


class ActivityDetailSerializer(ActivitySerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, activity):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return activity.like_set.filter(active=True).exists()

    class Meta:
        model = ActivitySerializer.Meta.model
        fields = ActivitySerializer.Meta.fields + ['liked']


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['statute', 'score']


class TrainingPointSerializer(serializers.ModelSerializer):
    scores = ScoreSerializer(many=True)

    class Meta:
        model = TrainingPoint
        fields = ['active', 'totalScore', 'student', 'scores']


class StatuteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statute
        fields = ['name', 'point', 'description']


class StudentSerializer(UserSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'clas', 'avatar']



class RegistrationSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = Registration
        fields = ['attended', 'activity', 'student']


class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = ['faculty', 'id', 'email', 'password', 'username']

    def create(self, validated_data):
        # Tạo một người dùng Assistant
        user = Assistant.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            faculty=validated_data['faculty'],
            role='assistant'  # Nếu bạn sử dụng role để phân biệt loại người dùng
        )
        return user


class CreateRegisterActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['student', 'activity']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['name']


class MissingPointsReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPointsReport
        fields = ['proof', 'approved', 'student', 'activity']


class CreateMissingPointsReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPointsReport
        fields = ['proof', 'student', 'activity']


class CommentSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'student']


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = ['id', 'name']
