# Generated by Django 5.0.5 on 2024-05-30 15:15

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diem', '0004_trainingpoint_quyche_alter_student_avatar'),
    ]

    operations = [
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
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='quyche',
            options={'verbose_name_plural': 'Quy Chế'},
        ),
        migrations.AlterField(
            model_name='student',
            name='avatar',
            field=models.ImageField(upload_to='diem/%Y/%m'),
        ),
    ]
