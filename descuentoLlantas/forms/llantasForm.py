from django import forms

from descuentoLlantas.models import Marca


class LlantasForm(forms.Form):
    marca = forms.ModelChoiceField(Marca.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control col'}), required=False, empty_label="Marca")
