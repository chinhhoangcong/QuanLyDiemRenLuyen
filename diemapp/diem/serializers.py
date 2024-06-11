from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    # faculty = FacultySerializer()
    fullname = serializers.SerializerMethodField(source='fullname')
    # avatar = serializers.SerializerMethodField(source='avatar')

    # def get_avatar(self, user):
    #     return user.avatar.url

    def get_fullname(self, user):
        return user.last_name + user.first_name


# class UserDetailSerializer(UserSerializer):
#     major = serializers.SerializerMethodField(source='major')
#     committees = serializers.SerializerMethodField(source='committees')
#
#     def get_major(self, user):
#         if user.role == 'student':
#             return user.student.major.name
#
#         return None


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'active']


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['statute','score']


class TrainingPointSerializer(serializers.ModelSerializer):
    scores = ScoreSerializer(many=True)

    class Meta:
        model = TrainingPoint
        fields = ['active', 'totalScore', 'student','scores']


class StatuteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statute
        fields = ['name', 'point','description']


class StudentSerializer(UserSerializer):

    class Meta:
        model = Student
        fields = ['fullname','clas']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['attended', 'activity' ]



class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['name']


class MissingPointsReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPointsReport
        fields = ['proof','approved','student','activity']


