# Generated by Django 2.2.28 on 2023-11-13 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20231113_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipements',
            name='nom_equi',
            field=models.CharField(choices=[('Zone_d_attente', "Zone d'attente"), ('Zone_de_livraison', 'Zone de livraison'), ('Atelier_de_réparation', 'Atelier de réparation'), ('Atelier_de_diagnostic', 'Atelier de diagnostic')], default='__', max_length=200),
        ),
    ]
