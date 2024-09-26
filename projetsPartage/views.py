from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Project, Users  # Importer ton modèle
from .forms import UserRegistrationForm, UserLoginForm
import json

# Create your views here.

def ma_vue(request):
    # Interroger la base de données pour obtenir tous les utilisateurs
    projects = Project.objects.all().values()  # Obtenir tous les utilisateurs sous forme de dictionnaires

    # Convertir les résultats en liste
    projects_list = list(projects)

    return JsonResponse(projects_list, safe=False)  # Utiliser safe=False pour autoriser une liste


@csrf_exempt  # Pour désactiver la vérification CSRF (à éviter en production sans une autre mesure de sécurité)
def addProject(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Charger les données JSON du corps de la requête

            # Créer un nouvel enregistrement dans la base de données
            project = Project(
                title=data['title'],
                description=data['description'],
                username=data['username'],
                objectif=data['objectif'],
                category=data['category'],
                vote=data['vote'],
                image=data['image']
            )
            project.save()  # Sauvegarder l'enregistrement

            return JsonResponse({'message': 'Projet ajouté avec succès !'}, status=201)  # Réponse 201 pour la création réussie
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)  # Réponse 400 pour une mauvaise demande
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)  # Réponse 400 pour un JSON invalide
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)  # Réponse 405 pour méthode non autorisée


@csrf_exempt
def addUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = UserRegistrationForm(data)

            if form.is_valid():
                user = form.save()  # Sauvegarder l'utilisateur
                token = user.create_token() 
                return JsonResponse({'message': 'Utilisateur ajouté avec succès !', 'token': token}, status=201)
            else:
                return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = UserLoginForm(data)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                
                user = Users.objects.get(username=username)
                if check_password(password, user.password):
                    token = user.create_token()  # Créer le token
                    return JsonResponse({'message': 'Login successful', 'token': token}, status=200)
                else:
                    return JsonResponse({'error': 'Invalid credentials'}, status=401)
            else:
                return JsonResponse({'errors': form.errors}, status=400)

        except Users.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

from .models import Management

def getCountdownEnd(request):
    management = Management.objects.first()  # Récupère le premier enregistrement
    if management:
        return JsonResponse({'countdown_end': management.deadline}, status=200)
    return JsonResponse({'error': 'Aucun enregistrement trouvé'}, status=404)