# Generated by Django 5.1 on 2024-08-29 21:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes_app', '0009_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='recipes_app.status'),
        ),
    ]
