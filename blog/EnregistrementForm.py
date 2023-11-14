from django import forms
from .models import Vehicule, Equipements

class NewEnregistrementForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields=['marque','etat','lieu','type',]

    

class NewLieuForm(forms.ModelForm):
    class Meta :
        model = Equipements
        fields=['nom_equi','etat_equ',]