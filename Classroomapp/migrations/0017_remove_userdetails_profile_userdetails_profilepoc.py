# Generated by Django 5.0.3 on 2024-03-24 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Classroomapp', '0016_rename_dp_userdetails_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='profile',
        ),
        migrations.AddField(
            model_name='userdetails',
            name='profilepoc',
            field=models.FileField(default='1', upload_to=''),
        ),
    ]