# Generated by Django 5.1.1 on 2024-12-12 07:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_delete_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('registration_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
