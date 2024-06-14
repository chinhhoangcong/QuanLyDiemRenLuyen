from enum import Enum
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from cloudinary.models import CloudinaryField


# Create your models here.


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True, null=True)

    class Meta:
        abstract = True


class UserRole(Enum):
    MANAGER = 'manager'
    ASSISTANT = 'assistant'
    STUDENT = 'student'


class User(AbstractUser):
    role = models.CharField(UserRole, max_length=20, null=True)
    avatar = CloudinaryField('avatar', null=True)

    def __str__(self):
        return self.last_name + self.first_name


class Student(User):
    clas = models.ForeignKey('Class', on_delete=models.RESTRICT, related_name='students', null=True)
    activity = models.ManyToManyField('Activity', through='Registration', related_name='student')

    class Meta:
        verbose_name_plural = 'Sinh viên'


class Assistant(User):
    faculty = models.ForeignKey('Faculty', on_delete=models.RESTRICT, default=True, null=False)

    class Meta:
        verbose_name_plural = 'Trợ Lý Sinh Viên'


class Manager(User):
    class Meta:
        verbose_name_plural = 'Chuyên Viên Cộng Tác Sinh Viên'


class Faculty(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Khoa'


class Class(BaseModel):
    name = models.CharField(max_length=50, null=True)
    faculty = models.ForeignKey('Faculty', on_delete=models.RESTRICT, related_name='clas', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Lớp'


class Statute(BaseModel):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    point = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Quy Chế'


class TrainingPoint(BaseModel):
    totalScore = models.CharField(max_length=25, null=True)
    statute = models.ManyToManyField(Statute, through="Score", related_name="QuyChe")
    student = models.ForeignKey(Student, on_delete=models.RESTRICT, related_name='TrainingPoint', null=True)

    def __str__(self):
        return self.student.last_name + self.student.first_name

    class Meta:
        verbose_name_plural = 'Bảng điểm rèn luyện'


class Score(BaseModel):
    score = models.CharField(max_length=25, null=True)
    statute = models.ForeignKey(Statute, on_delete=models.RESTRICT, related_name='scores')
    trainingPoint = models.ForeignKey(TrainingPoint, on_delete=models.RESTRICT, related_name='scores')
    student = models.ForeignKey(Student, on_delete=models.RESTRICT, related_name='scores', null=True)

    def __str__(self):
        return self.student.last_name + self.student.first_name + ' - ' + self.statute.name + ' - ' + self.score

    class Meta:
        unique_together = ('statute', 'trainingPoint')
        verbose_name_plural = 'Điểm sinh viên theo từng quy chế'


class Activity(BaseModel):
    name = models.CharField(max_length=50, null=False)
    description = RichTextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Hoạt Động Ngoại Khóa'


class Registration(BaseModel):
    attended = models.BooleanField(default=False, null=True)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT, related_name='registration')
    activity = models.ForeignKey(Activity, on_delete=models.RESTRICT, related_name='registration')

    def __str__(self):
        return f"{self.student} - {self.activity}"

    class Meta:
        verbose_name_plural = 'Đăng kí Hoạt Động Ngoại Khóa'


class MissingPointsReport(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT, related_name='MissingPointsReport', default=False)
    activity = models.ForeignKey(Activity, on_delete=models.RESTRICT, related_name='MissingPointsReport', default=False)
    proof = models.CharField(max_length=255, null=True, default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.activity} - {'Approved' if self.approved else 'Đang chờ xử lý'}"

    class Meta:
        verbose_name_plural = 'Danh Sách Báo Thiếu'


class Achievements(BaseModel):
    name = models.CharField(max_length=50, null=True)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT, related_name="achievements")

    def __str__(self):
        return f"{self.student} - {self.name} "

    class Meta:
        verbose_name_plural = 'Thành Tích Ngoại Khóa'


class Interaction(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=False)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255, null=False)


class Like(Interaction):
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'activity')
