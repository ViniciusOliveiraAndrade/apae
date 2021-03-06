from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'social'
urlpatterns = [
    
    path('', views.index, name='index'),

    path('Perfil', views.perfil, name='perfil'),

        
    #Triagens
    path('Realizar_Triagem', views.triagem_realizar, name='triagem_realizar'),
    path('Cadastrar_Triagem', views.cadastrar_triagem, name='cadastrar_triagem'),
    path('Editar_Triagem/<int:triagem_id>', views.triagem_editar, name='triagem_editar'),
    path('Edit_Triagem', views.editar_triagem, name='editar_triagem'),
    path('Listar_Triagem', views.triagem_listar, name='triagem_listar'),
    path('Detalhe_Triagem/<int:triagem_id>', views.triagem_detalhe, name='triagem_detalhe'),

    #Usuario
    path('Listar_Usuarios/', views.usuarios_listar, name='usuarios_listar'),
    path('InativarUsuario', views.inativar_usuario, name='inativar_usuario'),
    path('InativarUsuario/<int:user_id>', views.inativar_usuario, name='inativar_usuario'),
    path('AtivarUsuario', views.ativar_usuario, name='ativar_usuario'),
    path('AtivarUsuario/<int:user_id>', views.ativar_usuario, name='ativar_usuario'),
    
    #visitas
    path('Agendar_Visita/<int:usuario_id>', views.visita_agendar, name='visita_agendar'),
    path('Listar_Visita', views.visita_listar, name='visita_listar'),
    path('Editar_Visita/<int:visita_id>', views.visita_editar, name='visita_editar'),

    #Eventos
    path('Cadastrar_Eventos', views.evento_cadastrar, name='evento_cadastrar'),
    path('Editar_Eventos/<int:evento_id>', views.evento_editar, name='evento_editar'),
    path('Listar_Eventos', views.evento_listar, name='evento_listar'),
    path('Subir_Lista/<int:evento_id>/<int:lista_id>', views.subir, name='subir'),
    path('Descer_Lista/<int:evento_id>/<int:lista_id>', views.descer, name='descer'),
    path('Remover_Lista/<int:evento_id>/<int:lista_id>', views.removerLista, name='removerLista'),
    path('Adicionar_Usuario/<int:evento_id>', views.addUsuario, name='addUsuario'),
    path('add_Lista', views.addLista, name='addLista'),
    path('salvarData', views.salvarData, name='salvarData'),
    path('salvarHora', views.salvarHora, name='salvarHora'),


    #CID
    path('cadastrarCID', views.cadastrarCID, name='cadastrarCID'),
]