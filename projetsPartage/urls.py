from django.urls import path
from .views import ma_vue, addProject, addUser, loginUser, getCountdownEnd  # Assure-toi d'importer la vue que tu as créée

urlpatterns = [
    path('', ma_vue, name='ma_vue'),  # '/ma-route/' est l'URL qui appelle ma_vue
    path('addProject', addProject, name='addProject'),
    path('addUser', addUser, name='addUser'),
    path('login', loginUser, name='loginUser'),  # Ajoute cette ligne
    path('getCountdownEnd', getCountdownEnd, name='getCountdownEnd'),  # Ajoute cette ligne
]