from django import forms
 
from .models import Vehicule
 
class MoveForm(forms.ModelForm):
 
    class Meta:
        model = Vehicule
        fields = ('lieu',)

