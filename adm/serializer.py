
from rest_framework import serializers
from .models import *


# class UsuarioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Usuario
#         fields = ['identifier','date_of_birth','foto','height','password']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        # fields = ('id','identifier','nome','nomeSocial','date_of_birth','foto')
        fields = ('id','identifier','nome','nomeSocial','date_of_birth')

class CartoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartoes
        fields =('id', 'conta', 'tipo', 'numero', 'bandeira',)
# class ClientePFSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClientePF
#         fields = ('cliente','cpf','rg')

# class ClientePJSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClientePJ
#         fields = ('cliente', 'cnpj', 'inscricaoEstadual', 'inscricaoMunicipal')

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ('id','cliente','logradouro','numero','bairro','cidade','uf','cep','complemento')

class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato
        fields = ('id','cliente','numero','email', 'observacao')

class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ('id','cliente','agencia','numero','chavePix','saldo','limite','updated_at','ativa')

class MovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = ('id','remetente','remetenteNome','destinatario','destinatarioNome','chavePix','tipo','valor','data','descricao',)

class InvestimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investimento
        fields = ('id','conta', 'valor', 'prazo', 'saldoInvestido', 'local', 'finalizado')

class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields = ('id', 'conta', 'valor', 'juros','observacao', 'data', 'valorPagar', 'aprovado',)

class ParcelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcelas
        fields = ('id','emprestimo','vezes','valorParcela','dataPagamento','valorPago')
