from django import forms

class nameSpaceForm(forms.Form):
    namespace = forms.CharField(label='namespace', max_length=20, required=True)
    keys = forms.CharField(label='keys', max_length=50, required=True)
    redistype=forms.CharField(label='redistype', max_length=1, required=True)