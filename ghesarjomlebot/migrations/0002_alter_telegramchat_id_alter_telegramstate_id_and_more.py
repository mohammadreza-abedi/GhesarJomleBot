# Generated by Django 4.0.6 on 2022-07-13 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ghesarjomlebot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramchat',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='telegramstate',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
