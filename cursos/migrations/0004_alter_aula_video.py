# Generated by Django 3.2 on 2021-06-11 22:13

from django.db import migrations
import efbclass.storage.fields
import efbclass.storage.storage_vimeo


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0003_categoria_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aula',
            name='video',
            field=efbclass.storage.fields.VimeoField(blank=True, help_text='Enviar para o Vimeo - Teste', null=True, storage=efbclass.storage.storage_vimeo.VimeoFileStorage, upload_to=''),
        ),
    ]
