# Generated by Django 5.0.3 on 2024-04-05 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Classroomapp', '0033_rating_email_alter_rating_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecontent',
            name='rating',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
