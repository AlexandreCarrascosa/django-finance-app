# Generated by Django 3.2.5 on 2021-11-18 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='totalBalance',
            fields=[
                ('bank', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Banco')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Saldo')),
            ],
            options={
                'db_table': 'totalBalance',
            },
        ),
    ]