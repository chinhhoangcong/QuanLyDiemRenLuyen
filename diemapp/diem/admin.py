from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from .models import *
from django.urls import path
from . import dao


class TrainingPointAdminSite(admin.AdminSite):
    site_header = 'Quản Lý Điểm Rèn Luyện'

    def get_urls(self):
        return [
            path('diem-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        faculty = request.GET.get('faculty')
        clas = request.GET.get('class')
        return TemplateResponse(request, 'admin/stats.html', {
            'stats_faculty': dao.get_training_core_by_faculty(faculty_name=faculty),
            'stats_class': dao.get_training_score_by_class(class_name=clas)
        })


admin_site = TrainingPointAdminSite(name="myapp")


class UserAdmin(admin.ModelAdmin):
    fields = ['avatar', 'first_name', 'last_name', 'username', 'password', 'email']

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)

        super().save_model(request, obj, form, change)


class StudentAdmin(UserAdmin):
    list_display = ['pk', 'first_name', 'last_name', 'clas']
    fields = UserAdmin.fields + ['clas'] + ['img']
    readonly_fields = ['img']

    def img(self, student):
        if student:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=student.avatar.name)
            )

    def save_model(self, request, obj, form, change):
        obj.role = UserRole.STUDENT.value

        super().save_model(request, obj, form, change)


class AssistantAdmin(UserAdmin):
    list_display = ['pk', 'first_name', 'last_name']
    fields = UserAdmin.fields

    def save_model(self, request, obj, form, change):
        obj.role = UserRole.ASSISTANT.value

        super().save_model(request, obj, form, change)


class ManagerAdmin(UserAdmin):
    list_display = ['pk', 'first_name', 'last_name']
    fields = UserAdmin.fields

    def save_model(self, request, obj, form, change):
        obj.role = UserRole.MANAGER.value

        super().save_model(request, obj, form, change)


class StatuteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'point']


class TrainingPointAdmin(admin.ModelAdmin):
    list_display = ['pk', 'student', 'totalScore']


class ScoreAdmin(admin.ModelAdmin):
    fields = ['score', 'statute', 'trainingPoint', 'student']


admin_site.register(Statute, StatuteAdmin)
admin_site.register(TrainingPoint, TrainingPointAdmin)
admin_site.register(Student, StudentAdmin)
admin_site.register(Faculty)
admin_site.register(Score, ScoreAdmin)
admin_site.register(Activity)
admin_site.register(Class)
admin_site.register(Registration)
admin_site.register(MissingPointsReport)
admin_site.register(Achievements)
admin_site.register(Assistant, AssistantAdmin)
admin_site.register(Manager, ManagerAdmin)
