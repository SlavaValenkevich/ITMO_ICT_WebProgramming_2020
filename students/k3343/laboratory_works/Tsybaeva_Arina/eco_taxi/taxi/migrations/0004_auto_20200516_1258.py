# Generated by Django 3.0.4 on 2020-05-16 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0003_delete_costclient'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Имя категории')),
                ('cost', models.IntegerField(verbose_name='Цена сдачи мусора на переработку')),
                ('category', models.ManyToManyField(to='taxi.Category')),
            ],
            options={
                'verbose_name': 'Цена для клиента',
                'verbose_name_plural': 'Цены для клиента',
            },
        ),
        migrations.CreateModel(
            name='CostFabric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.PositiveIntegerField(verbose_name='Цена сдачи мусора на переработку заводу')),
                ('name', models.CharField(max_length=20, verbose_name='Имя категории')),
                ('category', models.ManyToManyField(to='taxi.Category')),
            ],
            options={
                'verbose_name': 'Цена для завода',
                'verbose_name_plural': 'Цены для завода',
            },
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
