# Generated by Django 3.0.6 on 2020-05-31 13:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('climber_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='climbing',
            name='climbing_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
