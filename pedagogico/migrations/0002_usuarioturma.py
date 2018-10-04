# Generated by Django 2.1.1 on 2018-09-24 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedagogico', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioTurma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedagogico.Turma')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedagogico.Usuario')),
            ],
        ),
    ]
