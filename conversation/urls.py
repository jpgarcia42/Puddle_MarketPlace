from django.urls import path # CORRIGIDO: Agora importando do lugar certo
from . import views

app_name = 'conversation'

urlpatterns = [
    path('new/<int:item_pk>/', views.new_conversation, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('inbox/', views.inbox, name='inbox'),
]