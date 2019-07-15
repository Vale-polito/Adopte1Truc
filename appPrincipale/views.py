from django.shortcuts import render
#from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect
from datetime import datetime
from django.shortcuts import get_object_or_404
from appPrincipale.models import Categorie,Objet,Comentaire
from .forms import ObjetForm, ComentaireForm, ConnexionForm, SignUpForm,SignUpModifierForm
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.core.files import File
from datetime import datetime

import json



gros_mon=[" putain "," merde "," chier "," enculer "," batard "," salaud "," salope "," connard "," connasse "," connard "]

# Create your views here.
#voir MonObjet et les images


def test_generique(request):
	return render(request,'appPrincipale/test_vu_generique.html')

def ajax_recherche(request):
	if request.is_ajax():
		if request.method=="GET":
			print(request)
			string_titre_catgorie = request.GET.get("r_categorie","Toutes")
			nom_article = request.GET.get("article","-1")
			code_postal = request.GET.get("code_postal","Toutes")
			print(string_titre_catgorie)
			print(nom_article)
			print(code_postal)
			#macat=Categorie.objects.filter(titre=string_titre_catgorie)
			if string_titre_catgorie != "Toutes" and nom_article != "" and code_postal!="Toutes":
				objets = Objet.objects.filter(categorie__titre=string_titre_catgorie).filter(Q(nom__contains = nom_article) |Q( description__contains = nom_article) & Q(code_postal__contains = code_postal))
			elif string_titre_catgorie != "Toutes" and nom_article != "" and code_postal=="Toutes":
				objets = Objet.objects.filter(categorie__titre=string_titre_catgorie).filter(Q(nom__contains = nom_article) |Q( description__contains = nom_article))

			elif (string_titre_catgorie != "Toutes") and (nom_article == "") and code_postal!="Toutes":
				objets = Objet.objects.filter(Q(categorie__titre=string_titre_catgorie)&Q(code_postal__contains = code_postal))
			elif (string_titre_catgorie != "Toutes") and (nom_article == "") and code_postal=="Toutes":
				objets = Objet.objects.filter(categorie__titre=string_titre_catgorie)

			elif (string_titre_catgorie == "Toutes") and (nom_article != "") and code_postal!="Toutes":
				print("recherche que postal et article")
				objets = Objet.objects.filter(Q(nom__contains = nom_article) | Q( description__contains = nom_article)&Q(code_postal__contains = code_postal))
			elif (string_titre_catgorie == "Toutes") and (nom_article != "") and code_postal=="Toutes":
				objets = Objet.objects.filter(Q(nom__contains = nom_article) |Q( description__contains = nom_article))
			elif (string_titre_catgorie == "Toutes") and (nom_article == "") and code_postal!="Toutes":
				print("recherche que postal")
				objets = Objet.objects.filter(Q(code_postal__contains = code_postal))
			else:
				objets = Objet.objects.all()
		return render(request, 'appPrincipale/ajx_work.html', locals())

	else :
		return redirect(new_work)

def more(request):
	if request.is_ajax():
		if request.method=="GET":
			print("reques",request)
			comp=request.GET.get("c");
			print(comp);
			com=int(comp)
			print(datetime.now().day)

			objets=Objet.objects.all()[com*3:(com+1)*3]
			print(objets)
			return render(request, 'appPrincipale/ajx_work.html',locals())
	else :
		return redirect(new_work)

def new_blog(request):
    error = False
    categories = Categorie.objects.all()
    objets = Objet.objects.all()

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    nom = request.user.username
                    connecte_good=True
                    return render(request, 'appPrincipale/index.html', locals())
                else:
                    error = True
    else:
        nom = request.user.username
        form = ConnexionForm()
    return render(request, 'appPrincipale/blog.html', locals())

#affiche le profil du gars
def new_about(request):
	nom=request.user.username
	if(nom != ''):
		user=request.user
		objets=Objet.objects.filter(user=request.user)

		#si je recois un post ca veut dire que j'ai recu une demande pour supprimer un objet
		if request.method=="POST":
			print("recu post")
			objets=Objet.objects.filter(user=request.user)
			objet_id=request.POST.get("objet_id")
			print(objet_id)
			objet=Objet.objects.get(id=objet_id)
			objet.delete()
		return render(request, 'appPrincipale/about.html',locals())
	else:
		return redirect(se_connecter)
#ajouter un nouvel objet
def new_contact(request):
	nom = request.user.username
	if(nom != ''):
		categories = Categorie.objects.all()
		objets = Objet.objects.all()
		nom = request.user.username
		code_false=False
		objet_false=False
		objet_cree=False
		if request.method=="POST":
			print(request.POST)
			form=ObjetForm(request.POST, request.FILES)
			print("MA FORM: ", form, "*********************")
			if form.is_valid():
				print("test forme est valide")


				Nom=form.cleaned_data['nom']
				Description=form.cleaned_data['description']

				bol_vulgaire=False
				description=Description.lower()
				for word in gros_mon :

					if word in description:
						bol_vulgaire=True
						return render(request, 'appPrincipale/new_objet.html', locals())
				nom=Nom.lower()
				for word in gros_mon :
					if word in nom:
						bol_vulgaire=True
						return render(request, 'appPrincipale/new_objet.html', locals())

				code_postal=request.POST.get("code_postal")
				photo=request.POST.get("photo")
				print(photo)
				try:
					print("try")
					int(code_postal)
					if len(code_postal)==5:
						objet=form.save(commit=False)
						objet.user=request.user
						if objet.categorie.titre =="Loisirs":
							objet.photo="/photos/loisirs.png"
						elif objet.categorie.titre=="Vehicules":
							objet.photo="photos/vehicules.png"
						elif objet.categorie.titre=="Immobilier":
							objet.photo="photos/pret_immo.png"
						elif objet.categorie.titre=="Vacances":
							objet.photo="photos/vacances.png"
						elif objet.categorie.titre=="Multimedia":
							objet.photo="photos/multimedia.png"
						elif objet.categorie.titre=="Services":
							objet.photo="photos/services.png"
						elif objet.categorie.titre=="Maison":
							objet.photo="photos/interieur.png"
						elif objet.categorie.titre=="Professionnel":
							objet.photo="photos/pro.png"
						print(objet.photo)
						objet.save()
						objet_cree=True
						return render(request, 'appPrincipale/index.html', locals())
					else:
						code_false=True
				except ValueError:
					code_false=True
					print("c'est pas un int")
					return render(request, 'appPrincipale/new_objet.html',locals())
			else:
				print("form pas valid")
				objet_false=True
		return render(request, 'appPrincipale/new_objet.html',locals())
	else:
		return redirect(se_connecter)

def new_index(request):
    nom=request.user.username
    categories = Categorie.objects.all()
    objets = Objet.objects.all()[0:3]
    return render(request, 'appPrincipale/index.html',locals())

def new_services(request):
    nom = request.user.username
    categories = Categorie.objects.all()
    objets = Objet.objects.all()
    return redirect('/accueil/index',locals())

#affiche l'article avec les commentaireq
def new_article(request):
	nom = request.user.username
	user=request.user
	categories = Categorie.objects.all()
	peut_commenter=True
	if request.method=="GET":
		objets = Objet.objects.all()[0:3]
		return render(request, 'appPrincipale/index.html',locals())
	if request.method == "POST":
		objet_image = request.POST.get("objet_image")
		objet_id=request.POST.get("objet_id")
		objet=Objet.objects.get(id=objet_id)

		if objet.user.id == request.user.id:
			peut_supprimer= True
			peut_commenter = False

		commentaires=Comentaire.objects.filter(object_id=objet_id)
		return render(request, 'appPrincipale/services.html',locals())


def new_work(request):
    nom = request.user.username
    categories = Categorie.objects.all()
    if request.method=="GET":
        objets = Objet.objects.all()[0:3]
    if request.method == "POST":
        string_titre_catgorie = request.POST.get("Titre_Categorie","Toutes")
        nom_article = request.POST.get("Nom_Article","-1")
        code_postal = request.POST.get("code_postal","Toutes")
        print(string_titre_catgorie)
        print(nom_article)
        print(code_postal)
        #macat=Categorie.objects.filter(titre=string_titre_catgorie)
        if string_titre_catgorie != "Toutes" and nom_article != "" and code_postal!="Toutes":
            objets = Objet.objects.filter(categorie__titre=string_titre_catgorie).filter(Q(nom__contains = nom_article) |Q( description__contains = nom_article) & Q(code_postal__contains = code_postal))
        elif string_titre_catgorie != "Toutes" and nom_article != "" and code_postal=="Toutes":
            objets = Objet.objects.filter(categorie__titre=string_titre_catgorie).filter(Q(nom__contains = nom_article) |Q( description__contains = nom_article))

        elif (string_titre_catgorie != "Toutes") and (nom_article == "") and code_postal!="Toutes":
            objets = Objet.objects.filter(Q(categorie__titre=string_titre_catgorie)&Q(code_postal__contains = code_postal))
        elif (string_titre_catgorie != "Toutes") and (nom_article == "") and code_postal=="Toutes":
            objets = Objet.objects.filter(categorie__titre=string_titre_catgorie)

        elif (string_titre_catgorie == "Toutes") and (nom_article != "") and code_postal!="Toutes":
            print("recherche que postal et article")
            objets = Objet.objects.filter(Q(nom__contains = nom_article) | Q( description__contains = nom_article)&Q(code_postal__contains = code_postal))
        elif (string_titre_catgorie == "Toutes") and (nom_article != "") and code_postal=="Toutes":
            objets = Objet.objects.filter(Q(nom__contains = nom_article) |Q( description__contains = nom_article))
        elif (string_titre_catgorie == "Toutes") and (nom_article == "") and code_postal!="Toutes":
            print("recherche que postal")
            objets = Objet.objects.filter(Q(code_postal__contains = code_postal))
        else:
            objets = Objet.objects.all()
    return render(request, 'appPrincipale/work.html', locals())

#formulaire d'inscription
def signup(request):

    nom = request.user.username
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(request.POST)
        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'appPrincipale/inscription.html', {'form': form})


def modifier_profil(request):
	nom=request.user.username
	if(nom != ''):
		user=request.user
		form = SignUpModifierForm(request.POST or None)
		if request.method == 'POST':
			print(request.POST)
			if form.is_valid():


				user.first_name=form.cleaned_data['first_name']
				user.last_name=form.cleaned_data['last_name']
				user.email=form.cleaned_data['email']


				user.save()

				user = authenticate(username=user.username, password=user.password)
				login(request, user)
				return redirect(new_about)
			print("pas valide")
		return render(request, 'appPrincipale/modifier_profil.html', {'form': form})
	else:
		return redirect(se_connecter)

def logout_view(request):

    auth.lougout(request)
    deconnect=True
    #auth.lougout(request)
    return redirect(new_index)



def new_commentaire(request):
	nom=request.user.username

	if(nom != ''):
		form=ComentaireForm(None)
		object_id=0
		if request.method=="GET":
			objet_id=request.GET.get("objet_id","-1")
			print(objet_id)
			print("jai un get")

		if request.method=="POST":
			print("j'ai un post")
			print(request.POST)
			form=ComentaireForm(request.POST)
			objet_id=request.POST.get("objet_id","-1")
			print(objet_id)
			if form.is_valid():
				print("form valide")
				Titre=form.cleaned_data['titre']
				Contenu=form.cleaned_data['contenu']
				error=form.errors.as_data()
				print(error)
				bol_vulgaire=False
				contenu=Contenu.lower()
				for word in gros_mon :

					if word in contenu:
						bol_vulgaire=True
						return render(request, 'appPrincipale/commentaire.html', locals())
				titre=Titre.lower()
				for word in gros_mon :
					if word in titre:
						bol_vulgaire=True
						return render(request, 'appPrincipale/commentaire.html', locals())

				if bol_vulgaire :
					rien=False
				else :
					print("pas vulgaire")
					comentaire=form.save(commit=False)

					objet=Objet.objects.get(id=objet_id)

					comentaire.content_object=objet
					comentaire.object_id=objet_id

					comentaire.save()
					envoie=True
					article_id=objet_id
					article=objet
					commentaires=Comentaire.objects.all()
					commentaire_poster=True
					return redirect(new_index)
		return render(request, 'appPrincipale/commentaire.html', locals())
	else:
		return redirect(se_connecter)

def supprimer_commentaire(request):
	nom=request.user.username
	if(nom != ''):
		categories=Categorie.objects.all()
		objets=Objet.objects.all()
		if request.method=="POST":
			commentaire_id=request.POST.get("commentaire_id")
			com=Comentaire.objects.get(id=commentaire_id)
			com.delete()
			commentaire_supprime=True
		return render(request , 'appPrincipale/work.html', locals())
	else:
		return redirect(se_connecter)



def se_connecter(request):
	return render(request , 'appPrincipale/se_connecter.html')

def apropos(request):
    return render(request , 'appPrincipale/apropos.html', locals())

def terms(request):
    return render(request , 'appPrincipale/terms.html', locals())




def modifier_objet(request):
	nom = request.user.username
	if(nom != ''):
		categories = Categorie.objects.all()
		nom = request.user.username
		code_false=False
		objet_cree=False
		if request.method=="POST":
			print(request.POST)
			form=ObjetForm(request.POST)
			print(request.POST)
			objet_id_a_modifier=request.POST.get("objet_id")
			print(objet_id_a_modifier)
			objet=Objet.objects.get(id=objet_id_a_modifier)

			if form.is_valid():
				print("test forme est valide")


				Nom=form.cleaned_data['nom']
				Description=form.cleaned_data['description']

				bol_vulgaire=False
				description=Description.lower()
				for word in gros_mon :

					if word in description:
						bol_vulgaire=True
						return render(request, 'appPrincipale/commentaire.html', locals())
				nom=Nom.lower()
				for word in gros_mon :
					if word in nom:
						bol_vulgaire=True
						return render(request, 'appPrincipale/commentaire.html', locals())

				code_postal=request.POST.get("code_postal")
				photo=request.POST.get("photo")
				print(photo)
				try:
					print("try")
					int(code_postal)
					if len(code_postal)==5:
						OBJET_buffer=form.save(commit=False)
						objet.categorie=OBJET_buffer.categorie
						objet.nom=OBJET_buffer.nom
						objet.description=OBJET_buffer.description
						objet.code_postal=OBJET_buffer.code_postal
						objet.adresse=OBJET_buffer.adresse

						print(objet.photo)

						objet.save()
						objet_cree=True
						objets=Objet.objects.filter(user=request.user)
						return render(request, 'appPrincipale/about.html', locals())
					else:
						code_false=True
				except ValueError:
					code_false=True
					print("c'est pas un int")
					return render(request, 'appPrincipale/new_objet.html',locals())
			else:
				print("form pas valid")

		return render(request, 'appPrincipale/modifier_objet.html',locals())
	else:
		return redirect(se_connecter)
