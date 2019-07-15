from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

	url(r'^blog/$', views.new_blog, name='blog'),
	url(r'^about/$', views.new_about, name='about'),
	url(r'^contact/$', views.new_contact, name='contact'),
	url(r'^commentaire/$', views.new_commentaire, name='commentaire'),
	url(r'^index/$', views.new_index, name='index'),
	url(r'^work/$', views.new_work, name='work'),
	url(r'^services/$', views.new_services, name='services'),
	url(r'^article/$', views.new_article, name='article'),
	
	url(r'^supprimer_commentaire/$', views.supprimer_commentaire, name='supprimer_commentaire'),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/accueil/index'}, name='logout'),

	url(r'^inscription/$', views.signup, name='inscription'),
	url(r'^apropos/$', views.apropos, name='apropos'),
	url(r'^terms/$', views.terms, name='terms'),
	
	url(r'^modifier_objet/$', views.modifier_objet, name='modifier_objet'),
	url(r'^modifier_profil/$', views.modifier_profil, name='modifier_profil'),
	url(r'^se_connecter/$', views.se_connecter, name='se_connecter'),
	
	url(r'work/ajax/$',views.more),
	url(r'work/ajax_recherche/$',views.ajax_recherche),
	url(r'index/ajax/$',views.more),
	



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
