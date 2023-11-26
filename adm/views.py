from django.shortcuts import render
from rest_framework.response import responses
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import viewsets
from django.http import HttpResponseBadRequest
from .models import *
from .serializer import *
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
# from .backends import AccountBlocked
import decimal

# class CustomLoginView(LoginView):
#     def form_valid(self, form):
#         try:
#             return super().form_valid(form)
#         except AccountBlocked as e:
#             return JsonResponse({'error': str(e)}, status=403)

def get_id(request):
    token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[1]
    dados = AccessToken(token)
    return dados["user_id"]

class CnpjCpfVerificar(RetrieveAPIView):
    queryset = Cliente.objects.all()
    serializer_class = Cliente

    def retrieve(self, request, *args, **kwargs):
        ident = self.kwargs['identifier']
        try:
            instance = Cliente.objects.get(identifier = ident)
        except:
            return Response({"exist": False}, 200)
        print(instance)
        data = {
            'exist': True if instance else False
        }
        # if instance.numero if instance else False:
        #     return Response({"exist": False}, 404)
        return Response(data)
class RgVerificar(RetrieveAPIView):
    queryset = Cliente.objects.all()
    serializer_class = Cliente

    def retrieve(self, request, *args, **kwargs):
        ident = self.kwargs['rg']
        try:
            instance = Cliente.objects.get(rg = ident)
        except:
            return Response({"exist": False}, 200)
        print(instance)
        data = {
            'exist': True if instance else False
        }
        # if instance.numero if instance else False:
        #     return Response({"exist": False}, 404)
        return Response(data)
class NumerosVerificar(RetrieveAPIView):
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer

    def retrieve(self, request, *args, **kwargs):
        ident = self.kwargs['numero']
        try:
            instance = Contato.objects.get(numero = ident)
        except:
            return Response({"exist": False}, 200)
        print(instance)
        data = {
            'exist': True if instance else False
        }
        # if instance.numero if instance else False:
        #     return Response({"exist": False}, 404)
        return Response(data)
    
class EmailsVerificar(RetrieveAPIView):
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer

    def retrieve(self, request, *args, **kwargs):
        ident = self.kwargs['email']
        try:
            instance = Contato.objects.get(email = ident)
        except:
            return Response({"exist": False}, 200)
        print(instance)
        data = {
            'exist': True if instance else False
        }
        return Response(data)

class ContaVerificarPix(ListAPIView):

    serializer_class = ContaSerializer

    def get_queryset(self):
        parametro = self.kwargs['chavePix']
        queryset = Conta.objects.filter(chavePix=parametro)
        return queryset

class ClienteList(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        usuario = get_id(request)
        print(usuario)
        conta = Conta.objects.get(id = usuario)
        
        return conta
    
    def create(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION','').split(' ')[1]
        print(token)
        return super().create(self, request, *args, **kwargs)

class ClienteDetail(RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteDetailB(RetrieveAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def retrieve(self, request, *args, **kwargs):
        ident = self.kwargs['identifier']
        try:
            instance = Cliente.objects.get(identifier = ident)
        except:
            return Response({"detail": "Not found."}, 404)
        print(instance)
        data = {
            'ativo': instance.is_active if instance else False
        }
        if instance.is_active if instance else False:
            return Response({"detail": "Not found."}, 404)
        return Response(data)

class CartoesList(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Cartoes.objects.all()
    serializer_class = CartoesSerializer
    
    def create(self, request, *args, **kwargs):
        id = get_id(request)
        conta = Conta.objects.get(cliente=id)
        print(conta)
        tipo = request.data['tipo']        

        if tipo == 'd' and Cartoes.objects.filter(conta=conta, tipo='d').exists():
            return HttpResponseBadRequest("Já existe um cartão do tipo 'debito' associado a esta conta.")
        
        if tipo == 'c' and Cartoes.objects.filter(conta=conta, tipo='c').exists() >= 5:
            return HttpResponseBadRequest("Limite máximo de cartões do tipo 'credito' atingido para esta conta.")
        
        if tipo == 'b' and Cartoes.objects.filter(conta=conta, tipo='b').exists():
            return HttpResponseBadRequest("Limite máximo de cartões do tipo 'crebito' atingido para esta conta.")
        
        numero = cartao()
        resposta = Cartoes.objects.create(conta=conta, tipo=tipo, numero=numero)
        
        return Response(CartoesSerializer(resposta).data,200)

class CartoesDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Cartoes.objects.all()
    serializer_class = CartoesSerializer

class EnderecoList(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
class EnderecoDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer



class ContatoList(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer
class ContatoDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer



class ContaList(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
class ContaDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer



class MovimentacaoList(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer

    def create(self, request, *args, **kwargs):
        contaRemetenteId = get_id(request)
        conta_remetente = Conta.objects.get(cliente=int(contaRemetenteId))

        print(request.data)
        conta_destinatario = Conta.objects.model
        # #pegar o token e obter o user_id
        # print("dest :",destinatario)
        try:
            conta_destinatario = Conta.objects.get(chavePix=request.data['chavePix'])
        
        except conta_destinatario.DoesNotExist:
            return Response({"Error":"This Pix Does not exist"},400)
        
        destinatario = conta_destinatario.cliente

        _mutable = request.POST._mutable

        if (decimal.Decimal(request.data['valor']) < 0):
            request.POST._mutable = True
            request.data['valor'] = decimal.Decimal(request.data['valor']) *-1
            request.POST._mutable = False
            request.POST._mutable = _mutable
        

        if conta_destinatario is None:
            raise serializers.ValidationError('destinatario nao exist')
        if conta_remetente is None:
            raise serializers.ValidationError('remetente nao exist')
        if conta_remetente.saldo <= decimal.Decimal(request.data['valor']):
            raise serializers.ValidationError('Saldo is not suficiente')
        
        if contaRemetenteId == conta_destinatario.id:
            raise serializers.ValidationError('conta e destinatario sao os mesmos')
        
        conta_remetente.saldo -= decimal.Decimal(request.data['valor'])
        conta_remetente.save()
        
        conta_destinatario.saldo += decimal.Decimal(request.data['valor'])
        conta_destinatario.save()

        

        # set to mutable
        request.POST._mutable = True
        request.data['remetente'] = contaRemetenteId
        request.data['remetenteNome'] = conta_remetente.cliente.nome
        request.data['destinatario'] = conta_destinatario.id
        request.data['destinatarioNome'] = destinatario.nome
        request.POST._mutable = False
        request.POST._mutable = _mutable
        # print("EESSEE :"+request.data['contaDestinatario']+" : "+contaRemetenteId)

        

        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        id_user = get_id(request)
        Conta.objects.get(id=id_user)
        movimentacoes = Movimentacao.objects.filter(Q(remetente=id_user) | Q(destinatario=id_user)).order_by("-data")
        
        return Response(MovimentacaoSerializer(movimentacoes, many=True).data)
    
class MovimentacaoDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer

class InvestimentoList(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Investimento.objects.all()
    serializer_class = MovimentacaoSerializer
class InvestimentoDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Investimento.objects.all()
    serializer_class = InvestimentoSerializer

# class ModelUpdateView(UpdateAPIView):
#     model = UsuarioSerializer
#     template_name = ".html"


# class UsuarioViews(viewsets.ModelViewSet):
#     serializer_class = UsuarioSerializer
#     def get_queryset(self):
#         queryset = Usuario.objects.all()
#         return queryset
    
    # def create(self, request, *args, **kwargs):
    #     dados =request.data
        
    #     criar = Usuario.objects.create(email=dados['email'])
    #     return super().create(request, *args, **kwargs)

class EmprestimoList(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer

    def create(self, request, *args, **kwargs):
        contaRemetenteId = get_id(request)
        conta_remetente = Conta.objects.get(cliente=int(contaRemetenteId))
        valorEmprestimo = float(request.data['valor'])
        juros = 0.05
        if (valorEmprestimo > 1500):
            juros = 0.1
        if (valorEmprestimo > 10000):
            juros = 0.3
        if (valorEmprestimo > 50000):
            juros = 0.5
        saldo = float(conta_remetente.saldo)

        _mutable = request.POST._mutable

        request.POST._mutable = True

        if (saldo*3.00 >= valorEmprestimo):
            conta_remetente.saldo += decimal.Decimal(valorEmprestimo)
            valorPagar = (valorEmprestimo)+(valorEmprestimo*juros)
            aprovado = True
            conta_remetente.save()
        else:
            request.data['conta'] = contaRemetenteId
            request.data['valor'] = valorEmprestimo
            request.data['juros'] = 0
            request.data['valorPagar'] = 0
            request.data['aprovado'] = False
            request.data['observacao'] = 'Este valor não é válido para emprestimo'
            request.POST._mutable = _mutable
            return super().create(request, *args, **kwargs)
        
        request.data['conta'] = contaRemetenteId
        request.data['valor'] = valorEmprestimo
        request.data['juros'] = juros
        request.data['valorPagar'] = valorPagar
        request.data['aprovado'] = aprovado
        request.POST._mutable = _mutable

        return super().create(request, *args, **kwargs)
    
class EmprestimoDetail(RetrieveUpdateDestroyAPIView):
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer



class ParcelasList(ListCreateAPIView):
    queryset = Parcelas.objects.all()
    serializer_class = ParcelasSerializer
class ParcelasDetail(RetrieveUpdateDestroyAPIView):
    queryset = Parcelas.objects.all()
    serializer_class = ParcelasSerializer


