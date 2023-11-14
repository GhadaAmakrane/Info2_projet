from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .forms import MoveForm 
from django.contrib import messages
from .form import VehiculeForm
from .EnregistrementForm import NewEnregistrementForm,NewLieuForm
from .models import Vehicule, Equipements

ListeEtats = [('arrivee', 'Arrivé'),
              ('bon_etat', 'En bon état'),
              ('en_diagnostic', 'En diagnostic'),
              ('en_reparation', 'En réparation'),
              ('en_attente_piece', 'En attente de pièces'),
              ('en_attente_de_récuperation', 'En attente de récupération')]

 
def acceuil(request):
    vehicule_en_attente = Vehicule.objects.filter(etat="en_attente_piece").count()
    vehicule_en_diagnostic = Vehicule.objects.filter(etat="en_diagnostic").count()
    vehicule_a_livre = Vehicule.objects.filter(etat="bon_etat").count()
    vehicule_en_reparation = Vehicule.objects.filter(etat=" en_reparation").count()

    return  render(request, 'blog/acceuil.html', {
        'vehicules_attente': vehicule_en_attente,
        'vehicules_diagnostic': vehicule_en_diagnostic,
        'vehicules_livraison': vehicule_a_livre,
        'vehicules_reparation': vehicule_en_reparation,
    })

def creer_vehicule(request):
    if request.method == 'POST':
        form = NewEnregistrementForm(request.POST)
        if form.is_valid():
            nouveau_vehicule = form.save(commit=False)
            nouveau_vehicule.etat = 'arrivee'  
            nouveau_vehicule.save()
            return redirect('vehicule_detail',nouveau_vehicule.id_vehicule) 
    else:
        form = VehiculeForm()

    return render(request, 'blog/creer_nouveau_vehicule.html', {'form': form})

def erreur_etat(request):
     return render(request, 'blog/erreur_changement_etat.html')


def creer_lieu(request):
    if request.method =='POST':
        form = NewLieuForm(request.POST)
        if form.is_valid():
            nouveau_lieu = form.save(commit=False)
            nouveau_lieu.etat_equi = 'Libre'  
            nouveau_lieu.save()
            return redirect('detail_equipement',nouveau_lieu.id_equipement)  
    else:
        form = NewLieuForm()
    
    return render(request, 'blog/creer_nouveau_equi.html', {'form': form})


def vehicule_list(request):
    vehicules = Vehicule.objects.all()
    return render(request, 'blog/vehicule_list.html', {'vehicules': vehicules})
 

def vehicule_detail(request, id_vehicule):
    vehicule = get_object_or_404(Vehicule, id_vehicule=id_vehicule)
    form=MoveForm()
    if form.is_valid():
        ancien_lieu = get_object_or_404(Equipements, id_equip=vehicule.lieu.id_equip)
        ancien_lieu.etat_equ = "libre"
        ancien_lieu.save()
        form.save()
        nouveau_lieu = get_object_or_404(Equipements, id_equip=vehicule.lieu.id_equipement)
        nouveau_lieu.etat_equ = "occupé"
        nouveau_lieu.save()
        return redirect('vehicule_detail', id_vehicule=id_vehicule)
    else:
        form = MoveForm()
        return render(request,
                  'blog/vehicule_detail.html',
                  {'vehicule': vehicule, 'lieu': vehicule.lieu, 'form': form})
    
def detail_equipement(request, id_equipement):
    lieu = get_object_or_404(Equipements, id_equipement=id_equipement)
    return render(request, 'blog/equipement_detail.html', {'lieu': lieu})

def equipement_list(request):
    equipements = Equipements.objects.all()
    return render(request, 'blog/equi_list.html', {'equipements': equipements})
 

def diagnostic(new_eta,old_etat):
    if (new_eta =="en_diagnostic" and old_etat =="arrivee"):
        return True
    return False 

def reparation_attente(new_eta,old_etat):
    if (old_etat =="en_diagnostic"  ):
        if (new_eta =="en_reparation"):
            return True
    elif(old_etat =="en_diagnostic"  ):
        if (new_eta =="en_attente_piece"):
            return True
    return False
        
def livraison(new_eta,old_etat,):
    if (new_eta =="en_attente_de_récuperation" and old_etat =="en_reparation"):
        return True
    return False 

def get_lieu_libre():
    return  Equipements.objects.filter(etat_equ='Libre')  
    

def modifier_vehicule(request,id_vehicule):
    vehicule = get_object_or_404(Vehicule, id_vehicule=id_vehicule)
    old_etat = vehicule.etat
    old_lieu = vehicule.lieu
    if request.method == 'POST':
        form = VehiculeForm(request.POST, instance=vehicule)
        if form.is_valid():
            nouvel_etat = form.cleaned_data['etat']
            if nouvel_etat=="en_diagnostic":
                if diagnostic(nouvel_etat,old_etat) :  
                    form.save()
                    lieux_diagnostic = Equipements.objects.filter(etat_equ='Libre', nom_equi="Atelier_de_diagnostic")
                    old_lieu.etat_equ='Libre'
                    old_lieu.save()
                    vehicule.lieu = lieux_diagnostic.first()
                    vehicule.lieu.etat_equ='Occupé'
                    vehicule.lieu.save()
                    return redirect('vehicule_detail', id_vehicule=id_vehicule)
                else: 
                    return redirect(erreur_etat)
            elif nouvel_etat=="en_reparation":

                if reparation_attente(nouvel_etat,old_etat):
                    form.save()
                    lieux_reparation = Equipements.objects.filter(etat_equ='Libre', nom_equi="Atelier_de_réparation")
                    old_lieu.etat_equ='Libre'
                    old_lieu.save()
                    vehicule.lieu = lieux_reparation.first()
                    vehicule.lieu.etat_equ ='Occupé'
                    vehicule.lieu.save()
                    return redirect('vehicule_detail', id_vehicule=id_vehicule)
                else: 
                    return redirect(erreur_etat)
                
            elif nouvel_etat=="en_attente_de_récuperation":
                if livraison(nouvel_etat,old_etat):
                    form.save()
                    lieux_livraison = Equipements.objects.filter(etat_equ='Libre', nom_equi="Zone_de_livraison")
                    old_lieu.etat_equ='Libre'
                    old_lieu.save()
                    vehicule.lieu = lieux_livraison.first()
                    vehicule.lieu.etat_equ = "Occupé"
                    vehicule.lieu.save()
                    return redirect('vehicule_detail', id_vehicule=id_vehicule)
                else: 
                    return redirect(erreur_etat)
            else:
                return redirect(erreur_etat)
                   
    else:
        form = VehiculeForm(instance=vehicule)

    return render(request, 'blog/vehicule_form.html', {'form': form, 'vehicule': vehicule})


def livrer_vehicule(request,id_vehicule):
    vehicule = get_object_or_404(Vehicule, id_vehicule=id_vehicule)

    if vehicule.etat == 'en_attente_de_récuperation':
        vehicule.delete()
        return redirect(vehicule_list)  
    else:
        return redirect(erreur_etat)
    
      



def succes_livraison(request):
    return render(request, 'blog/livraison_succes.html')  





  