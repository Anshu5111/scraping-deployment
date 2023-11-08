# Generated by Django 4.2.6 on 2023-11-02 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=264)),
                ('password', models.CharField(max_length=264)),
                ('email', models.EmailField(max_length=264, unique=True)),
            ],
        ),
    ]
