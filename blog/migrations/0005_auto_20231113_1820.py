# Generated by Django 2.2.28 on 2023-11-13 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_vehicule_date_creation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicule',
            name='etat',
            field=models.CharField(choices=[('arrivee', 'Arrivé'), ('bon_etat', 'En bon état'), ('en_diagnostic', 'En diagnostic'), ('en_reparation', 'En réparation'), ('en_attente_piece', 'En attente de pièces'), ('en_attente_de_récuperation', 'En attente de récuperation')], max_length=100),
        ),
    ]
