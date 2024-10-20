# Generated by Django 5.1.1 on 2024-10-11 23:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_rename_boards_board'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CardList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_lists', to='tasks.board')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cards', to=settings.AUTH_USER_MODEL)),
                ('card_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='tasks.cardlist')),
            ],
        ),
    ]