# Generated by Django 5.2 on 2025-05-13 01:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContaReceber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=8)),
                ('vencimento', models.DateField()),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('pago', 'Pago')], default='pendente', max_length=10)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studio.aluno')),
            ],
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pagamento', models.DateField()),
                ('metodo_pagamento', models.CharField(choices=[('PIX', 'PIX'), ('Cartão', 'Cartão'), ('Dinheiro', 'Dinheiro'), ('Transferência', 'Transferência')], max_length=20)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(default='Efetivado', max_length=20)),
                ('conta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='studio.contareceber')),
            ],
        ),
    ]
