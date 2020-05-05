# Generated by Django 2.1.5 on 2020-03-28 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_first_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeeksModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='carowner',
            name='cars',
            field=models.ManyToManyField(through='project_first_app.Owning', to='project_first_app.Car'),
        ),
    ]