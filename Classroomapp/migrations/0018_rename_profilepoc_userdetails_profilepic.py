# Generated by Django 5.0.3 on 2024-03-24 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Classroomapp', '0017_remove_userdetails_profile_userdetails_profilepoc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdetails',
            old_name='profilepoc',
            new_name='profilepic',
        ),
    ]
