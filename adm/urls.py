from django.urls import path
from . import views
from rest_framework import routers

router = routers.SimpleRouter()

# router.register('usuario', views.UsuarioViews , basename='Usuario')


urlpatterns = [
    
    path('clientes/', view=views.ClienteList.as_view()),
    path('clientes/<pk>/', view=views.ClienteDetail.as_view()),
    path('clientesB/<str:identifier>/', view=views.ClienteDetailB.as_view()),

    # path('clientesPF/', view=views.ClientePFList.as_view()),
    # path('clientesPF/<pk>/', view=views.ClientePFDetail.as_view()),
    

    path('cartoes/', view=views.CartoesList.as_view()),
    path('cartoes/<pk>/', view=views.CartoesDetail.as_view()),

    path('contatos/', view = views.ContatoList.as_view()),
    path('contatos/<pk>/', view = views.ContatoDetail.as_view()),

    path('enderecos/', view = views.EnderecoList.as_view()),
    path('enderecos/<pk>/', view = views.EnderecoDetail.as_view()),
    
    path('contas/', view = views.ContaList.as_view()),
    path('contas/<pk>/', view = views.ContaDetail.as_view()),
    path('contas/<str:chavePix>', view=views.ContaVerificarPix.as_view()),

    
    path('movimentacao/', view = views.MovimentacaoList.as_view()),
    path('movimentacao/<pk>/', view = views.MovimentacaoDetail.as_view()),
    
    path('investimento/', view = views.InvestimentoList.as_view()),
    path('investimento/<pk>/', view = views.InvestimentoDetail.as_view()),
    
    path('emprestimo/', view = views.EmprestimoList.as_view()),
    path('emprestimo/<pk>/', view = views.EmprestimoDetail.as_view()),
    
    path('parcelas/', view = views.ParcelasList.as_view()),
    path('parcelas/<pk>/', view = views.ParcelasDetail.as_view()),

    path('cnpjcpf/<str:identifier>', view=views.CnpjCpfVerificar.as_view()),
    path('rg/<str:rg>', view=views.RgVerificar.as_view()),
    path('numeros/<str:numero>', view=views.NumerosVerificar.as_view()),
    path('emails/<str:email>', view=views.EmailsVerificar.as_view()),
    
]+router.urls