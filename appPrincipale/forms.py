from __future__ import unicode_literals
from django import forms
from .models import Objet, Comentaire
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ObjetForm(forms.ModelForm):
    class Meta:
        model = Objet
        exclude=('photo',)
    def clean(self):
        cleaned_data = super(ComentaireForm, self).clean()
        nom= cleaned_data.get('nom')
        description = cleaned_data.get('description')
        return cleaned_data


class ComentaireForm(forms.ModelForm):
    class Meta:
        model = Comentaire
        #fields = '__all__'
        exclude=('content_type','object_id','content_object','user')
    def clean(self):
        cleaned_data = super(ComentaireForm, self).clean()
        titre = cleaned_data.get('titre')
        contenu = cleaned_data.get('contenu')
        raise forms.ValidationError("nique")
        self.add_error("contenu","va nqieur")
        return cleaned_data





class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label = "Prenom", max_length=30)
    last_name = forms.CharField(label = "Nom de famille", max_length=30)
    email = forms.EmailField(max_length=254, help_text='Requis. Entrez une adresse mail valide.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class SignUpModifierForm(forms.Form):

    first_name = forms.CharField(label = "Prenom", max_length=30)
    last_name = forms.CharField(label = "Nom de famille", max_length=30)
    email = forms.EmailField(max_length=254, help_text='Requis. Entrez une adresse mail valide.')
