# Generated by Django 3.2.5 on 2021-11-18 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_totalbalance_register_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='moneyOutputs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('description', models.TextField(blank=True, null=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor')),
                ('output_date', models.DateField(verbose_name='Data de compra')),
                ('payment_type', models.CharField(choices=[('CV', 'Credit at sigth'), ('CP', 'Credit in installments'), ('D', 'Debit')], max_length=10)),
                ('installments', models.DecimalField(decimal_places=0, max_digits=2, verbose_name='Parcelas')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.totalbalance')),
            ],
        ),
        migrations.CreateModel(
            name='moneyInputer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Origem')),
                ('value', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor')),
                ('input_date', models.DateField(verbose_name='Data de pagamento')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.totalbalance')),
            ],
        ),
    ]
