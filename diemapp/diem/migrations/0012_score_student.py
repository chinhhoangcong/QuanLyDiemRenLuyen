# Generated by Django 5.0.1 on 2024-06-02 06:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diem', '0011_alter_class_options_alter_major_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='scores', to='diem.student'),
        ),
    ]