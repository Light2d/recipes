# Generated by Django 5.1 on 2024-08-26 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes_app', '0002_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='time',
            field=models.CharField(max_length=20),
        ),
    ]
