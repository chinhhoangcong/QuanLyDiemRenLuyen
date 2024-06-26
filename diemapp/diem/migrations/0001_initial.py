# Generated by Django 5.0.1 on 2024-06-12 03:46

import ckeditor.fields
import cloudinary.models
import diem.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(max_length=20, null=True, verbose_name=diem.models.UserRole)),
                ('avatar', cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='avatar')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True, null=True)),
                ('name', models.CharField(max_length=50)),
                ('description', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name_plural': 'Hoạt Động Ngoại Khóa',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Khoa',
            },
        ),
        migrations.CreateModel(
            name='Statute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('point', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Quy Chế',
            },
        ),
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Trợ Lý Sinh Viên',
            },
            bases=('diem.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Chuyên Viên Cộng Tác Sinh Viên',
            },
            bases=('diem.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Sinh viên',
            },
            bases=('diem.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('faculty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='clas', to='diem.faculty')),
            ],
            options={
                'verbose_name_plural': 'Lớp',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True, null=True)),
                ('attended', models.BooleanField(default=False)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='registration', to='diem.activity')),
            ],
            options={
                'verbose_name_plural': 'Đăng kí Hoạt Động Ngoại Khóa',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True, null=True)),
                ('score', models.CharField(max_length=25, null=True)),
                ('statute', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='scores', to='diem.statute')),
            ],
            options={
                'verbose_name_plural': 'Điểm sinh viên theo từng quy chế',
            },
        ),
        migrations.CreateModel(
            name='TrainingPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True, null=True)),
                ('totalScore', models.CharField(max_length=25, null=True)),
                ('statute', models.ManyToManyField(related_name='QuyChe', through='diem.Score', to='diem.statute')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='TrainingPoint', to='diem.student')),
            ],
            options={
                'verbose_name_plural': 'Bảng điểm rèn luyện',
            },
        ),
        migrations.AddField(
            model_name='score',
            name='trainingPoint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='scores', to='diem.trainingpoint'),
        ),
        migrations.AddField(
            model_name='student',
            name='activity',
            field=models.ManyToManyField(related_name='student', through='diem.Registration', to='diem.activity'),
        ),
        migrations.AddField(
            model_name='student',
            name='clas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='students', to='diem.class'),
        ),
        migrations.AddField(
            model_name='score',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='scores', to='diem.student'),
        ),
        migrations.AddField(
            model_name='registration',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='registration', to='diem.student'),
        ),
        migrations.CreateModel(
            name='MissingPointsReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True, null=True)),
                ('proof', models.CharField(default=False, max_length=255, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('activity', models.ForeignKey(default=False, on_delete=django.db.models.deletion.RESTRICT, related_name='MissingPointsReport', to='diem.activity')),
                ('student', models.ForeignKey(default=False, on_delete=django.db.models.deletion.RESTRICT, related_name='MissingPointsReport', to='diem.student')),
            ],
            options={
                'verbose_name_plural': 'Danh Sách Báo Thiếu',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField()),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diem.activity')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diem.student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True, null=True)),
                ('content', models.CharField(max_length=255)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diem.activity')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diem.student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Achievements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='achievements', to='diem.student')),
            ],
            options={
                'verbose_name_plural': 'Thành Tích Ngoại Khóa',
            },
        ),
        migrations.AlterUniqueTogether(
            name='score',
            unique_together={('statute', 'trainingPoint')},
        ),
    ]
