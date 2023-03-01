from django import forms
from sostenimientos.models.factura import Factura


class SostenimientoForm(forms.Form):
    JUSTIFICACION = (
        ("1", "Todos"),
        ("2", "Justificados"),
        ("3", "Injustificados"),
        # ("4", "Pendientes")
    )
    factura = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col', 'placeholder': 'Factura'}), required=False)
    ean = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col ml-3', 'placeholder': 'EAN'}
    ), required=False)
    justificacion = forms.ChoiceField(choices=JUSTIFICACION, widget=forms.Select(
        attrs={'class': 'form-control col ml-3'}), required=False)
