# Generated by Django 5.0.6 on 2024-05-25 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BalduApp', '0003_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
