from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Equipements(models.Model):
    listeEquipement =  [
        ('Zone_d_attente', "Zone d'attente"),
        ('Zone_de_livraison', "Zone de livraison"),
        ('Atelier_de_réparation', "Atelier de réparation"),
        ('Atelier_de_diagnostic', "Atelier de diagnostic"),
    ]

    liste_etat_equi= [
        ('Libre','Libre'),
        ('Occupé','Occupé'),
    ]
    
    id_equipement = models.AutoField(primary_key=True)
    nom_equi =models.CharField(max_length=200, choices=listeEquipement, default='__')
    etat_equ=models.CharField(max_length=100, choices=liste_etat_equi)

    def get_id_equi(self):
        return self.id_equipement
    
    def get_nom_equi(self):
        return self.nom_equi
    
    def get_etat_equi(self):
        return self.etat_equ
    
    def __str__(self):
        return f"{self.id_equipement} {self.nom_equi} {self.etat_equ} "

    def verifie_disponibilité(self):
        try :
            if self.etat_equ == "Occupé":
                raise self.etat_equ
        except ValueError as e:
            print(e)
    
        return self.etat_equ
    
    def get_vehicule_at_lieu(self):
        try:
            return Vehicule.objects.get(lieu=self.nom_equi)
        except Vehicule.DoesNotExist:
            return None
    
    

class Vehicule(models.Model):
    ListeEtats= [('arrivee', 'Arrivé'),
        ('bon_etat', 'En bon état'),
        ('en_diagnostic', 'En diagnostic'),
        ('en_reparation', 'En réparation'),
        ('en_attente_piece', 'En attente de pièces'),
        ('en_attente_de_récuperation', 'En attente de récuperation')]
    
    ListeTypes= [('voiture', 'Voiture'),
        ('moto', 'Moto'),
        ('camion', 'Camion'),]

    id_vehicule = models.AutoField(primary_key=True)
    etat = models.CharField(max_length=100,choices=ListeEtats)
    type = models.CharField(max_length=100 , choices=ListeTypes)
    marque = models.CharField(max_length=200)
    lieu = models.ForeignKey(Equipements, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateField(default=timezone.now)

    def get_etat(self):
        return self.etat
    
    def get_id_vehicule(self):
        return self.id_vehicule
    
    def get_type(self):
        return self.type

    def get_marque(self):
        return self.marque
    
    
    
    def __str__(self):
        return f"{self.id_vehicule} {self.marque} {self.type} - {self.etat} "
    
    
    def Changer_lieu(self, nouv_lieu):
        lieu_occupe = Equipements.objects.filter(nom_equi=nouv_lieu, etat_equ='Occupé')
    
        if lieu_occupe.exists():
            print("Désolé, le lieu est déjà occupé")
        else:
            self.lieu = nouv_lieu
            self.save()
            print(f"Lieu du véhicule mis à jour à '{nouv_lieu.etat_equ}'")





