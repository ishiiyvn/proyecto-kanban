# Generated by Django 5.1.2 on 2024-12-11 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_remove_cardlist_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='due_date',
            field=models.DateTimeField(blank=True, default='1900-01-01 00:00'),
        ),
    ]
