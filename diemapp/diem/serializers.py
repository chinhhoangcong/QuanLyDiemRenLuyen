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

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password(data['password'])
        user.save()
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
        fields = ['first_name', 'last_name', 'clas']


class RegistrationSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = Registration
        fields = ['attended', 'activity', 'student']


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
