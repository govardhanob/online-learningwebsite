# Generated by Django 5.0.3 on 2024-03-24 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Classroomapp', '0004_alter_userdetails_dp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='dp',
            field=models.FileField(upload_to=''),
        ),
    ]
