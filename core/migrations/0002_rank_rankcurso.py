# Generated by Django 3.2 on 2021-07-17 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('empresa', models.CharField(max_length=50)),
                ('usuario', models.CharField(max_length=25)),
                ('nome', models.CharField(max_length=100)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar')),
                ('qtd_acertos', models.BigIntegerField()),
                ('qtd_perguntas', models.BigIntegerField()),
                ('data_ultima_prova', models.DateTimeField()),
                ('pontuacao', models.FloatField()),
                ('posicao', models.BigIntegerField()),
            ],
            options={
                'db_table': 'core_ranks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RankCurso',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('empresa', models.CharField(max_length=50)),
                ('nome_curso', models.CharField(max_length=100)),
                ('usuario', models.CharField(max_length=25)),
                ('nome', models.CharField(max_length=100)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar')),
                ('qtd_acertos', models.BigIntegerField()),
                ('qtd_perguntas', models.BigIntegerField()),
                ('data_ultima_prova', models.DateTimeField()),
                ('pontuacao', models.FloatField()),
                ('posicao', models.BigIntegerField()),
            ],
            options={
                'db_table': 'core_ranks_curso',
                'managed': False,
            },
        ),
    ]
