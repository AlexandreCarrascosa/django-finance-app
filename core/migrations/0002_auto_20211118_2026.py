# Generated by Django 3.2.5 on 2021-11-18 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalbalance',
            name='account',
            field=models.CharField(default=1, max_length=8, primary_key=True, serialize=False, verbose_name='Conta'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='totalbalance',
            name='bank',
            field=models.CharField(max_length=100, verbose_name='Banco'),
        ),
    ]