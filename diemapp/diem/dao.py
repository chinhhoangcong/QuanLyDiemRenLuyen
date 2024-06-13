from django.db.models import *
from .models import *


def get_training_core_by_faculty(faculty_name):
    scores_by_faculty = Student.objects.filter(clas__faculty__name=faculty_name) \
        .values('first_name', 'clas__faculty__name', 'TrainingPoint__totalScore')

    return scores_by_faculty


# Truy vấn điểm rèn luyện theo lớp
def get_training_score_by_class(class_name):
    scores_by_class = Student.objects.filter(clas__name=class_name) \
        .values('first_name', 'clas__name', 'TrainingPoint__totalScore')

    return scores_by_class


def get_training_score_by_achievements(achieve_name):
    scores_by_class = Student.objects.filter(achievements__name=achieve_name) \
        .values('first_name', 'achievements__name', 'TrainingPoint__totalScore')

    return scores_by_class
