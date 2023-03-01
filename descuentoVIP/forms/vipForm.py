from django import forms

from descuentoVIP.models import Vip, Categoria


class VipForm(forms.Form):
    cliente = forms.ModelChoiceField(Vip.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control col'}), required=False, empty_label="Cliente")

    categoria = forms.ModelChoiceField(Categoria.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control col ml-3'}), required=False, empty_label="Categoría")

    documento = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col ml-3', 'placeholder': '# Documento'}), required=False)
