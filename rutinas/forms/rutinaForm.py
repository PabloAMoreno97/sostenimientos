from django import forms
from rutinas.models.vehiculo import Vehiculo
from rutinas.models.articulo import TipoArticulo


class RutinaForm(forms.Form):
    vehiculo = forms.ModelChoiceField(Vehiculo.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control col'}), required=False, empty_label="Vehículo")
    articulo = forms.CharField(label='EAN', max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control col ml-3', 'placeholder': 'Ingresar EAN'}), required=False)
    tipo = forms.ModelChoiceField(TipoArticulo.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control col ml-3'}), required=False, empty_label="Tipo Artículo")
