# Generated by Django 5.1.2 on 2024-10-11 20:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0003_boards"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Boards",
            new_name="Board",
        ),
    ]