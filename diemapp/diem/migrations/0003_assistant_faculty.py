# Generated by Django 5.0.1 on 2024-06-13 06:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diem', '0002_alter_like_active_alter_like_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='assistant',
            name='faculty',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.RESTRICT, to='diem.faculty'),
        ),
    ]