# Generated by Django 5.0.3 on 2024-04-06 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Classroomapp', '0036_coursedetails_total_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='courseid',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='whishlist',
            name='courseid',
            field=models.IntegerField(),
        ),
    ]