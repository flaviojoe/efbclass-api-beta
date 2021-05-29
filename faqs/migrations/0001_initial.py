# Generated by Django 3.2 on 2021-05-11 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('modificado_em', models.DateTimeField(auto_now=True)),
                ('pergunta', models.CharField(max_length=200)),
                ('resposta', models.TextField(blank=True, null=True)),
                ('criado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faqs_faq_criadopor', to=settings.AUTH_USER_MODEL)),
                ('modificado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faqs_faq_modificadopor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'FAQ - Fale Conosco',
                'verbose_name_plural': 'FAQs - Fale Conosco',
            },
        ),
    ]
