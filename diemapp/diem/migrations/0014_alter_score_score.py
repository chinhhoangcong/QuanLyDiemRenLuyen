# Generated by Django 5.0.1 on 2024-06-02 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diem', '0013_remove_score_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
