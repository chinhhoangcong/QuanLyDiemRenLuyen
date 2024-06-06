# Generated by Django 5.0.1 on 2024-06-03 07:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diem', '0019_alter_score_score'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Major',
            new_name='Faculty',
        ),
        migrations.RemoveField(
            model_name='student',
            name='major',
        ),
        migrations.AddField(
            model_name='class',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='clas', to='diem.faculty'),
        ),
    ]
