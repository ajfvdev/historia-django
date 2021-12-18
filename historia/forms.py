from django import forms

class UploadFileForm(forms.Form):
    nombre = forms.TextInput()
    fecha = forms.DateField()
    file = forms.FileField()