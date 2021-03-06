# Generated by Django 3.2 on 2021-05-13 10:20

from django.db import migrations, models
import efbclass.storage.fields
import efbclass.storage.storage_vimeo


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aula',
            name='arquivo_video',
            field=models.FileField(blank=True, help_text='Enviar para o Storage padrão', null=True, upload_to='aulas_video'),
        ),
        migrations.AlterField(
            model_name='aula',
            name='url',
            field=models.URLField(blank=True, help_text='O link pode ser do Youtube ou Vimeo', verbose_name='Link do vídeo'),
        ),
        migrations.AlterField(
            model_name='aula',
            name='video',
            field=efbclass.storage.fields.VimeoField(blank=True, help_text='Enviar para o Vimeo', null=True, storage=efbclass.storage.storage_vimeo.VimeoFileStorage, upload_to=''),
        ),
    ]
