# Generated by Django 5.2 on 2025-05-12 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('rg', models.CharField(blank=True, max_length=20)),
                ('nome', models.CharField(max_length=100)),
                ('telefone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('data_nascimento', models.DateField()),
                ('status', models.BooleanField(default=True)),
                ('funcao', models.CharField(max_length=100)),
                ('salario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('carga_horaria', models.FloatField()),
                ('horarios_trabalho', models.JSONField(default=list)),
                ('login', models.CharField(max_length=50, unique=True)),
                ('senha_hash', models.CharField(max_length=128)),
                ('is_admin', models.BooleanField(default=False)),
                ('ultimo_acesso', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Plano',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField(unique=True)),
                ('nome', models.CharField(max_length=100)),
                ('qtd_aulas', models.IntegerField()),
                ('valor_aula', models.FloatField()),
                ('status', models.BooleanField(default=True)),
                ('limite_vigencia', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modalidade', models.CharField(max_length=50)),
                ('niveis_dificuldade', models.CharField(choices=[('Iniciante', 'Iniciante'), ('Intermediário', 'Intermediário'), ('Avançado', 'Avançado')], max_length=30)),
                ('descricao', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('rg', models.CharField(blank=True, max_length=20)),
                ('nome', models.CharField(max_length=100)),
                ('telefone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('data_nascimento', models.DateField()),
                ('status', models.BooleanField(default=True)),
                ('profissao', models.CharField(max_length=100)),
                ('historico_saude', models.TextField()),
                ('data_inicio_plano', models.DateField()),
                ('data_vencimento_plano', models.DateField()),
                ('plano_ativo', models.BooleanField(default=True)),
                ('evolucao', models.TextField(blank=True, null=True)),
                ('plano', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='studio.plano')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
