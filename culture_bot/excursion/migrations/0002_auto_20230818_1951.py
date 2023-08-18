# Generated by Django 2.2.19 on 2023-08-18 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('excursion', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exhibit',
            options={'verbose_name': 'Экспонат', 'verbose_name_plural': 'Экспонаты'},
        ),
        migrations.AlterModelOptions(
            name='reviewonexhibit',
            options={'verbose_name': 'Комментарий на экспонат', 'verbose_name_plural': 'Комментарии на экспонаты'},
        ),
        migrations.AlterModelOptions(
            name='reviewonroute',
            options={'verbose_name': 'Комментарий на маршрут', 'verbose_name_plural': 'Комментарии на маршруты'},
        ),
        migrations.AlterModelOptions(
            name='route',
            options={'verbose_name': 'Маршрут', 'verbose_name_plural': 'Маршруты'},
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='address',
            field=models.CharField(max_length=200, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='author',
            field=models.CharField(max_length=50, verbose_name='Художник'),
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='description',
            field=models.TextField(verbose_name='Описание экспоната'),
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название экспоната'),
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='rating',
            field=models.IntegerField(verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='route',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exhibit', to='excursion.Route', verbose_name='Маршрут'),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='author',
            field=models.CharField(max_length=20, verbose_name='Комментатор'),
        ),
        migrations.AlterField(
            model_name='route',
            name='description',
            field=models.TextField(verbose_name='Описание экспоната'),
        ),
        migrations.AlterField(
            model_name='route',
            name='rating',
            field=models.IntegerField(verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='route',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Название маршрута'),
        ),
    ]
