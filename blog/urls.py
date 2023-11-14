from django.urls import path
from . import views

urlpatterns = [
    path('', views.acceuil, name='acceuil'),
    path('vehicule_list/',views.vehicule_list,name="vehicule_list"),
    path('creer_vehicule/',views.creer_vehicule,name="creer_vehicule"),
    path('creer_lieu/',views.creer_lieu,name="creer_lieu"),
    path('succes_livraison/', views.succes_livraison, name='succes_livraison'),
    path('erreur_etat/',views.erreur_etat,name="erreur_etat"),
    path('equi_list/',views.equipement_list,name="equipement_list"),
    path('vehicule/<str:id_vehicule>/', views.vehicule_detail, name='vehicule_detail'),
    path('livrer_vehicule/<str:id_vehicule>/', views.livrer_vehicule, name='livrer_vehicule'),
    path('equipement/<str:id_equipement>/', views.detail_equipement, name='detail_equipement'),
    path('modifier_vehicule/<int:id_vehicule>/', views.modifier_vehicule, name='modifier_vehicule'),
    ]