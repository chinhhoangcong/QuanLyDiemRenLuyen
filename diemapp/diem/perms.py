from rest_framework import permissions
from .models import *


class OwnerAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        student = Student.objects.get(id=user.id)
        return self.has_permission(request, view) and obj.student == request.user


class IsStudentAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        return bool(request.user.role == UserRole.STUDENT.value)


class IsStudentOfAuthenticated(IsStudentAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(self.has_permission(request, view) and obj.student_id == request.user.id)
