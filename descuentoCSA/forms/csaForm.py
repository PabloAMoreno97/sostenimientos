from django import forms

from descuentoCSA.models import Csa


class CsaForm(forms.Form):
    ORIGEN = (
        ("Todos", "Todos"),
        ("Repme", "Repme"),
        ("Ventanilla", "Ventanilla")
    )
    csa = forms.ModelChoiceField(Csa.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control col'}), required=False, empty_label="CSA")
    origen = forms.ChoiceField(choices=ORIGEN, widget=forms.Select(
        attrs={'class': 'form-control col ml-3'}), required=False)
    documento = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col ml-3', 'placeholder': '# Documento'}), required=False)
