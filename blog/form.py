from django import forms
from .models import Vehicule,Equipements

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields=['marque','etat','lieu']

    def __init__(self, *args, **kwargs):
        super(VehiculeForm, self).__init__(*args, **kwargs)
        self.fields['lieu'].queryset = Equipements.objects.filter(etat_equ="Libre")  
        self.fields['lieu'].label_from_instance = lambda obj: f"{obj.id_equipement} {obj.nom_equi}"

    


        


        


    
