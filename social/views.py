from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date, parse_time
from django.views import generic
from django.db.models import Q

from social.models import *
from core.models import *
from core.utilidades import *

import datetime



# Views
@login_required
def index(request):
    visitas = Visita.objects.filter(realizada=False)
    eventos = Evento.objects.all()[:5]
    dados = {"visitas":visitas, 'eventos':eventos}
    return render(request,'social/index.html', dados)

#----------------------------------------------------------------------------------------
#Perfil
@login_required
def perfil(request):
    if request.method == "POST":
        if request.POST['verificaimagem'] != "Sem Imagem" and request.POST['verificaimagem'] != request.user.funcionario.imagem_url:
            try:
                request.user.funcionario.imagem.delete(save=True)
                request.user.funcionario.imagem = request.FILES['imagem']
                request.user.funcionario.save()   
            except Exception as e:
                pass
        pnome, unome = getNomeFuncionario(request.POST['nome'])
        request.user.first_name = pnome
        request.user.last_name = unome
        request.user.email = request.POST['email']
        request.user.save()
        gerar_acao(request.user.funcionario,"Edição","Funcionario",request.user.funcionario.id)
    return render(request,'social/perfil.html')

    
#----------------------------------------------------------------------------------------
#Views da Triagem
@login_required
def triagem_realizar(request):
    cids= CID.objects.all().order_by('-codigo')
    args = {'cids':cids}
    return render(request,'social/triagem_realizar.html', args)

@login_required
def triagem_editar(request,triagem_id):
    t = get_object_or_404(Triagem,pk=triagem_id)
    cids= CID.objects.all().order_by('-codigo')
    args = {'cids':cids, 't':t}
    return render(request,'social/triagem_editar.html', args)

@login_required
def triagem_detalhe(request,triagem_id):
    t = get_object_or_404(Triagem,pk=triagem_id)
    return render(request,'social/triagem_detalhe.html', {'t':t})

@login_required
def triagem_listar(request):
    try:
        triagens = Triagem.objects.all()
    except Exception as e:
        u = Usuario()
        f = Funcionario()
        t = Triagem()
        t.usuario = u
        t.assinatura_proficinal = f
        triagens = [t]
        raise e
    for x in triagens:
        print(x.usuario.nome)

    return render(request,'social/triagem_listar.html', {'triagens' : triagens})

#controle de Tricagem
@login_required
def cadastrar_triagem(request):
    cid = CID.objects.get(codigo=request.POST['cid'])
    usuario = Usuario(nome=request.POST['nome'], cid=cid)

    try:
        data = request.POST['datanascimento']
        data = data.split('/')

        datanascimento = datetime.datetime(int(data[2]),int(data[1]),int(data[0]))
        usuario.data_nacimento = datanascimento
    except Exception as e:
        datanascimento = datetime.datetime(2000,1,1)
        usuario.data_nacimento = datanascimento

    try:
        usuario.imagem = request.FILES['imagem']   
    except Exception as e:
        pass

    
    triagem = Triagem()

    triagem.sus = request.POST['sus']
    
    #Especialista
    if request.POST['acompanhado'] == 'NÂO':
        triagem.acompanhamento_com_especialista = False
    else:
        triagem.acompanhamento_com_especialista = True

    triagem.especialista = request.POST['especialista']
    
    #Familiares
    triagem.nome_pai = request.POST['painome']
    triagem.idade_pai = request.POST['paiidade']
    triagem.profissao_pai = request.POST['paiprofissao']
    
    triagem.nome_mae = request.POST['maenome']
    triagem.idade_mae = request.POST['maeidade']
    triagem.profissao_mae = request.POST['maeprofissao']

    #Renda Familiar
    if 'bpc' not in request.POST:
        triagem.bpc = False
    else:
        triagem.bpc = True

    if 'bolsafamilia' not in request.POST:
        triagem.bolsa_familia = False
    else:
        triagem.bolsa_familia = True

    if 'aposentadoria' not in request.POST:
        triagem.aposentadoria = False
    else:
        triagem.aposentadoria = True


    valor = request.POST['valor']
    valor = valor.replace(',','.')
    triagem.renda_familiar = valor
    triagem.benediciario = request.POST['beneficiario']

    #Endereco
    triagem.cep = request.POST['cep']
    triagem.rua = request.POST['rua']
    triagem.numero_da_rua = request.POST['numero']
    triagem.bairro = request.POST['bairro']
    triagem.ponto_de_referencia = request.POST['ponto']
    triagem.cidade = request.POST['cidade']
    
    #Contato
    triagem.telefone = request.POST['telefone']
    triagem.celular = request.POST['celular']
    triagem.email = request.POST['email']

    #Ensino
    if request.POST['ensino'] == 'NÂO':
        triagem.estuda_ensino_regular = False
    else:
        triagem.estuda_ensino_regular = True

    triagem.qual = request.POST['qual']
    triagem.ano_estuda = request.POST['ano']
    triagem.turma_estuda = request.POST['turma']
    triagem.turno_estuda = request.POST['turno']

    #saude
    triagem.medicacao = request.POST['medicacao']

    if request.POST['fisio'] == 'NÂO':
        triagem.e_i_fisio = False
    else:
        triagem.e_i_fisio = True

    if request.POST['hidro'] == 'NÂO':
        triagem.e_i_hidro = False
    else:
        triagem.e_i_hidro = True
    
    if request.POST['fono'] == 'NÂO':
        triagem.e_i_fono = False
    else:
        triagem.e_i_fono = True

    if request.POST['to'] == 'NÂO':
        triagem.e_i_to = False
    else:
        triagem.e_i_to = True

    if request.POST['psi'] == 'NÂO':
        triagem.e_i_psi = False
    else:
        triagem.e_i_psi = True

    if request.POST['ondonto'] == 'NÂO':
        triagem.e_i_ondonto = False
    else:
        triagem.e_i_ondonto = True

    if request.POST['medico'] == 'NÂO':
        triagem.e_i_medico = False
    else:
        triagem.e_i_medico = True


    if request.POST['psicopedagoga'] == 'NÂO':
        triagem.e_i_psicopedagoga = False
    else:
        triagem.e_i_psicopedagoga = True



    if request.POST['pedagogia'] == 'NÂO':
        triagem.e_i_pedagogia = False
    else:
        triagem.e_i_pedagogia = True


    #Observacoes
    triagem.observacoes = request.POST['obs']
    funcionario = request.user.funcionario
    triagem.assinatura_proficinal = funcionario
    
    data = request.POST['datarealizacao']
    data = data.split(' ')

    data[0] = data[0].split('/')
    data[1] = data[1].split(':')

    datatriagem = datetime.datetime(int(data[0][2]),int(data[0][1]),int(data[0][0]))
    datatriagem.replace(hour=int(data[1][0]),minute=int(data[1][1]),second=int(data[1][2]))

    triagem.data_da_triagem = datatriagem

    usuario.save()
    triagem.usuario = usuario
    triagem.save()
    gerar_acao(request.user.funcionario,"Cadastro","Triagem",triagem.id)
    return HttpResponseRedirect(reverse('social:triagem_editar', args=(triagem.id,)))

@login_required
def editar_triagem(request):
    triagem = get_object_or_404(Triagem,pk=request.POST['id'])

    if request.POST['verificaimagem'] != "Sem Imagem" and request.POST['verificaimagem'] != triagem.usuario.imagem_url:
        try:
            triagem.usuario.imagem.delete(save=True)
            triagem.usuario.imagem = request.FILES['imagem']   
        except Exception as e:
            pass




    data = request.POST['datanascimento']
    data = data.split('/')
    datanascimento = datetime.datetime(int(data[2]),int(data[1]),int(data[0]))

    triagem.usuario.nome=request.POST['nome']
    cid = CID.objects.get(codigo=request.POST['cid'])
    triagem.usuario.cid=cid
    triagem.usuario.data_nacimento=datanascimento
    triagem.usuario.save()
    
    triagem.sus = request.POST['sus']
    
    #Especialista
    if request.POST['acompanhado'] == 'NÂO':
        triagem.acompanhamento_com_especialista = False
    else:
        triagem.acompanhamento_com_especialista = True

    triagem.especialista = request.POST['especialista']
    
    #Familiares
    triagem.nome_pai = request.POST['painome']
    triagem.idade_pai = request.POST['paiidade']
    triagem.profissao_pai = request.POST['paiprofissao']
    
    triagem.nome_mae = request.POST['maenome']
    triagem.idade_mae = request.POST['maeidade']
    triagem.profissao_mae = request.POST['maeprofissao']

    #Renda Familiar
    if 'bpc' not in request.POST:
        triagem.bpc = False
    else:
        triagem.bpc = True

    if 'bolsafamilia' not in request.POST:
        triagem.bolsa_familia = False
    else:
        triagem.bolsa_familia = True

    if 'aposentadoria' not in request.POST:
        triagem.aposentadoria = False
    else:
        triagem.aposentadoria = True

    valor = request.POST['valor']
    valor = valor.replace(',','.')
    triagem.renda_familiar = valor
    triagem.benediciario = request.POST['beneficiario']

    #Endereco
    triagem.cep = request.POST['cep']
    triagem.rua = request.POST['rua']
    triagem.numero_da_rua = request.POST['numero']
    triagem.bairro = request.POST['bairro']
    triagem.ponto_de_referencia = request.POST['ponto']
    triagem.cidade = request.POST['cidade']
    
    #Contato
    triagem.telefone = request.POST['telefone']
    triagem.celular = request.POST['celular']
    triagem.email = request.POST['email']

    #Ensino
    if request.POST['ensino'] == 'NÂO':
        triagem.estuda_ensino_regular = False
    else:
        triagem.estuda_ensino_regular = True
    
    triagem.qual = request.POST['qual']
    triagem.ano_estuda = request.POST['ano']
    triagem.turma_estuda = request.POST['turma']
    triagem.turno_estuda = request.POST['turno']


    #saude
    triagem.medicacao = request.POST['medicacao']

    if request.POST['fisio'] == 'NÂO':
        triagem.e_i_fisio = False
    else:
        triagem.e_i_fisio = True

    if request.POST['hidro'] == 'NÂO':
        triagem.e_i_hidro = False
    else:
        triagem.e_i_hidro = True
    
    if request.POST['fono'] == 'NÂO':
        triagem.e_i_fono = False
    else:
        triagem.e_i_fono = True

    if request.POST['to'] == 'NÂO':
        triagem.e_i_to = False
    else:
        triagem.e_i_to = True

    if request.POST['psi'] == 'NÂO':
        triagem.e_i_psi = False
    else:
        triagem.e_i_psi = True

    if request.POST['ondonto'] == 'NÂO':
        triagem.e_i_ondonto = False
    else:
        triagem.e_i_ondonto = True

    if request.POST['medico'] == 'NÂO':
        triagem.e_i_medico = False
    else:
        triagem.e_i_medico = True


    if request.POST['psicopedagoga'] == 'NÂO':
        triagem.e_i_psicopedagoga = False
    else:
        triagem.e_i_psicopedagoga = True



    if request.POST['pedagogia'] == 'NÂO':
        triagem.e_i_pedagogia = False
    else:
        triagem.e_i_pedagogia = True



    #Observacoes
    triagem.observacoes = request.POST['obs']
    triagem.save()
    gerar_acao(request.user.funcionario,"Edição","Triagem",triagem.id)
    return triagem_editar(request,triagem.id)

#--------------------------------------------------------------------------------------------
#Views do usuario
@login_required
def usuarios_listar(request):

    try:
        triagens = Triagem.objects.filter(usuario__situacao="Ativo")
    except Exception as e:
        u = Usuario()
        f = Funcionario()
        t = Triagem()
        t.usuario = u
        t.assinatura_proficinal = f
        triagens = [t]
        raise e
    

    return render(request,'social/usuario_listar.html', {'triagens' : triagens})

@login_required
def inativar_usuario(request,user_id):
    u = get_object_or_404(Usuario,pk=user_id)
    u.situacao = "Inativo"
    u.save()
    gerar_acao(request.user.funcionario,"Inativar","Usuario",u.id)
    return redirect("social:usuarios_listar")

@login_required
def ativar_usuario(request,user_id):
    u = get_object_or_404(Usuario,pk=user_id)
    u.situacao = "Ativo"
    u.save()
    gerar_acao(request.user.funcionario,"Ativar","Usuario",u.id)
    return redirect("social:triagem_listar")

#--------------------------------------------------------------------------------------------
#views da visita

@login_required
def visita_listar(request):
    try:
        visitas = Visita.objects.all()
    except Exception as e:
        u = Usuario()
        f = Funcionario()
        v = Visita()
        v.usuario = u
        v.funcionario = f
        visitas = [v]
        raise e
    return render(request,'social/visita_listar.html', {'visitas' : visitas})

@login_required
def visita_agendar(request,usuario_id):
    u = Usuario.objects.get(pk=usuario_id)
    f = Funcionario.objects.filter(Q(cargo__nome="Assistente social") | Q(cargo__nome="Coordenador(a) saúde") | Q(cargo__nome="Coordenador(a) assistência social") )
    t = Triagem.objects.get(usuario=u)
    local = "Rua: "+t.rua+", N° "+t.numero_da_rua+"  |Bairro: "+t.bairro+"   |Ponto de Referencia: "+t.ponto_de_referencia+"   |Cidade: "+t.cidade

    if request.method == "POST":
        
        usuario = Usuario.objects.get(pk=request.POST['usuario_id'])
        
        first_name, last_name = getNomeFuncionario(request.POST['funcionario'])
        funcionario = Funcionario.objects.get(user__first_name=first_name, user__last_name=last_name)
        
        try:
            data = request.POST['datavisita']
            data = data.split('-')
            datavisita = datetime.datetime(int(data[0]),int(data[1]),int(data[2]))
        except Exception as e:
            datavisita = datetime.datetime(2000,1,1)

        if request.POST['realizada'] == 'Sim':
            realizada = True
        else:
            realizada = False

        observacoes = request.POST['obs']
        local = request.POST['local']

        visita = Visita.objects.create(
            usuario=usuario,
            funcionario=funcionario,
            data_visita=datavisita,
            observacoes=observacoes,
            realizada=realizada,
            local=local
            )

        gerar_acao(request.user.funcionario,"Cadastro","Visita",visita.id)
        return HttpResponseRedirect(reverse('social:visita_editar', args=(visita.id,)))

    return render(request,'social/visita_agendar.html', {'usuario':u, 'funcionario':f, 'local': local})

@login_required
def visita_editar(request,visita_id):
    try:
        visita = Visita.objects.get(pk=visita_id)
    except Exception as e:
        raise e
    f = Funcionario.objects.filter(cargo__nome="Assistente social")

    if request.method == "POST":
        visita = Visita.objects.get(pk=request.POST['id'])
        first_name, last_name = getNomeFuncionario(request.POST['funcionario'])
        funcionario = Funcionario.objects.get(user__first_name=first_name, user__last_name=last_name)
        
        try:
            data = request.POST['datavisita']
            data = data.split('-')
            datavisita = datetime.datetime(int(data[0]),int(data[1]),int(data[2]))
        except Exception as e:
            datavisita = datetime.datetime(2000,1,1)

        if request.POST['realizada'] == 'Sim':
            realizada = True
        else:
            realizada = False

        observacoes = request.POST['obs']
        local = request.POST['local']
        visita.funcionario=funcionario
        visita.data_visita=datavisita
        visita.observacoes=observacoes
        visita.realizada=realizada
        visita.local=local
        
        visita.save()
        gerar_acao(request.user.funcionario,"Edição","Visita",visita.id)
        return HttpResponseRedirect(reverse('social:visita_editar', args=(visita.id,)))

    return render(request,'social/visita_editar.html', {'visita' : visita, 'funcionario': f})

#----------------------------------------------------------------------------------------------------
#Eventos
@login_required
def evento_cadastrar(request):
    if request.method == "POST":
        dataa = parse_date(request.POST['datainicio'])
        datab = parse_date(request.POST['datafim'])
        e = Evento.objects.create(nome = request.POST['nome'], data_inicio = dataa, data_fim = datab)
        gerar_acao(request.user.funcionario,"Cadastro","Evento",e.id)
        return HttpResponseRedirect(reverse('social:evento_editar', args=(e.id,)))
    return render(request,'social/evento_cadastrar.html',{})

@login_required
def evento_editar(request,evento_id):
    evento = Evento.objects.get(pk=evento_id)
    if request.method == "POST":

        dataa = parse_date(request.POST['datainicio'])

        datab = parse_date(request.POST['datafim'])
        evento.nome = request.POST['nome']
        evento.data_inicio = dataa
        evento.data_fim = datab
        evento.save()
        gerar_acao(request.user.funcionario,"Edição","Evento",evento.id)
        return HttpResponseRedirect(reverse('social:evento_editar', args=(evento.id,)))
    return render(request,'social/evento_editar.html',{'evento':evento})

@login_required
def evento_listar(request):
    eventos = Evento.objects.all()
    return render(request,'social/evento_listar.html', {'eventos' : eventos})

@login_required
def subir(request,evento_id, lista_id):
    evento = Evento.objects.get(pk=evento_id)
    lista = Lista.objects.get(pk=lista_id)
    
    listaDescer = evento.lista.get(posicao= (lista.posicao - 1))
    listaDescer.posicao = listaDescer.posicao + 1
    listaDescer.save()
    
    lista.posicao = lista.posicao - 1
    lista.save()
    evento.save()
    gerar_acao(request.user.funcionario,"Edição","Evento",evento.id)
    return HttpResponseRedirect(reverse('social:evento_editar', args=(evento.id,)))

@login_required
def descer(request,evento_id, lista_id):
    evento = Evento.objects.get(pk=evento_id)
    lista = Lista.objects.get(pk=lista_id)
    
    listaSubir = evento.lista.get(posicao= (lista.posicao + 1))
    listaSubir.posicao = listaSubir.posicao - 1
    listaSubir.save()
    
    lista.posicao = lista.posicao + 1
    lista.save()
    evento.save()
    gerar_acao(request.user.funcionario,"Edição","Evento",evento.id)
    return HttpResponseRedirect(reverse('social:evento_editar', args=(evento.id,)))

@login_required
def removerLista(request,evento_id, lista_id):
    evento = Evento.objects.get(pk=evento_id)
    lista = Lista.objects.get(pk=lista_id)
    posicao_deletado = lista.posicao
    lista.delete()

    for l in evento.lista.all():
        if l.posicao > posicao_deletado:
            l.posicao = (l.posicao - 1)
            l.save()

    
    evento.save()
    gerar_acao(request.user.funcionario,"Edição","Evento",evento.id)
    return HttpResponseRedirect(reverse('social:evento_editar', args=(evento.id,)))

@login_required
def addUsuario(request,evento_id):
    evento = Evento.objects.get(pk=evento_id)
    listas = evento.lista.all()
    usuarioListas = []

    for l in listas:
        usuarioListas.append(l.usuario)

    usuarios = Triagem.objects.all()

    if request.method == "POST":
        q = request.POST['q']
        usuarios = Triagem.objects.filter(Q(usuario__nome__contains=q) | Q(usuario__cid__codigo__contains=q) | Q(usuario__data_nacimento__contains=q) | Q(usuario__situacao__contains=q) | Q(nome_pai__contains=q) | Q(nome_mae__contains=q))


    usuariosEnviar = []

    for u in usuarios:
        if u.usuario not in usuarioListas:
            usuariosEnviar.append(u)
            print(u.usuario.nome)


    return render(request,'social/evento_addUsuario.html',{'evento':evento_id, 'usuarios':usuariosEnviar})

# @login_required
# def addLista(request):

#     evento_id = request.GET.get('evento', None)
#     usuario_id = request.GET.get('usuario', None)

#     print("ID do evento"+evento_id)
#     print("ID do usuario"+usuario_id)

#     evento = Evento.objects.get(pk=evento_id)
#     usuario = Usuario.objects.get(pk=usuario_id)

#     lista = Lista.objects.create(posicao=(evento.lista.all().count() + 1), usuario=usuario)
#     evento.lista.add(lista)
#     lista.save()
#     evento.save()

#     gerar_acao(request.user.funcionario,"Edição","Evento",evento.id)
#     data = {'adcionado': True}
#     return JsonResponse(data)

#----------------------------------------------------------------------------------------------------
# 
# AJAX
# 
# 
#----------------------------------------------------------------------------------------------------
#CID

@login_required
def cadastrarCID(request):
    codigo = request.GET.get('codigo', None)
   
    data = {'cadastrado': False, 'codigo':codigo}
    try:
        
        CID.objects.create(codigo=codigo,descricao="")
        data['cadastrado']=True
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse(data)
    


#----------------------------------------------------------------------------------------------------
#Evento

@login_required
def addLista(request):

    evento_id = request.GET.get('evento', None)
    usuario_id = request.GET.get('usuario', None)

    evento = Evento.objects.get(pk=evento_id)
    usuario = Usuario.objects.get(pk=usuario_id)

    lista = Lista.objects.create(posicao=(evento.lista.all().count() + 1), usuario=usuario)
    evento.lista.add(lista)
    lista.save()
    evento.save()

    gerar_acao(request.user.funcionario,"Edição","Evento",evento.id)
    data = {'adcionado': True}
    return JsonResponse(data)


@login_required
def salvarData(request):

    listaID = request.GET.get('lista', None)
    data = parse_date(request.GET.get('data', None))

    lista = Lista.objects.get(pk=listaID)
    lista.data = data
    lista.save()

    gerar_acao(request.user.funcionario,"Edição","Lista", listaID)
    data = {'erro': False}
    return JsonResponse(data)


@login_required
def salvarHora(request):

    listaID = request.GET.get('lista', None)
    hora = parse_time(request.GET.get('hora', None))


    lista = Lista.objects.get(pk=listaID)
    lista.hora = hora
    lista.save()

    gerar_acao(request.user.funcionario,"Edição","Lista", listaID)
    data = {'erro': False}
    return JsonResponse(data)
