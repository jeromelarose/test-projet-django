from rest_framework_simplejwt.tokens import RefreshToken  # Ajoute cet import
from django.db import models
from django import forms


# Create your models here.
class Users(models.Model):
    id = models.AutoField(primary_key=True)  # Champ id personnalisé (auto-increment)
    username = models.CharField(max_length=150, unique=True)  # Champ pour le nom d'utilisateur, unique
    password = models.CharField(max_length=128)               # Champ pour le mot de passe (hashé, si possible)
    mail = models.EmailField(unique=True)                     # Champ pour l'email, unique
    picture = models.URLField(blank=True, null=True)         # Champ pour l'URL de l'image de profil
    def create_token(self):
        refresh = RefreshToken.for_user(self)  # Crée le token
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    class Meta:
        db_table = 'users'  # Spécifie le nom de la table existante
    def __str__(self):
        return self.username  # Représentation en chaîne de caractères

class Project(models.Model):
    id = models.AutoField(primary_key=True)  # Champ id personnalisé (auto-increment)
    title = models.CharField(max_length=255)  # Titre du projet
    description = models.TextField()  # Description du projet
    username = models.CharField(max_length=150)  # Nom de l'utilisateur
    objectif = models.IntegerField()  # Objectif
    category = models.CharField(max_length=100)  # Catégorie
    vote = models.IntegerField(default=0)  # Nombre de votes
    image = models.URLField(max_length=200)  # URL de l'image
    class Meta:
        db_table = 'problems'  # Spécifie le nom de la table existante
    def __str__(self):
        return self.title  # Pour afficher le titre dans l'admin

class Management(models.Model):
    id = models.AutoField(primary_key=True)  # Champ id personnalisé (auto-increment)
    countdown_end = models.DateTimeField()    # Champ pour stocker la date et l'heure de fin du compte à rebours

    class Meta:
        db_table = 'management'  # Spécifie le nom de la table si nécessaire

    def __str__(self):
        return f"Management ID: {self.id}, Countdown ends at: {self.countdown_end}"
    

class Management(models.Model):
    id = models.AutoField(primary_key=True)
    deadline = models.DateTimeField()  # Exemple pour stocker une date de fin
    
    class Meta:
        db_table = 'management'  # Nom de la table

    def __str__(self):
        return f'Management {self.id}'