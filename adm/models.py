from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from rest_framework import status, serializers
from django.utils import timezone
from validate_docbr import CPF, CNPJ
from rest_framework.response import Response 
from .sorteador import *


class CustomUserManager(BaseUserManager):
    def create_user(self, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """     

        identifier = extra_fields.get('identifier')

        cpf = CPF()
        cnpj = CNPJ()
        if not (cpf.validate(identifier) or cnpj.validate(identifier)):
            raise serializers.ValidationError({'identifier':["CPF/CNPJ is invalid"]})
            # raise ValueError(_("CPF/CNPJ is invalid"))
        #     # raise Response({'erro':"CPF/CNPJ is invalid"},status=status.HTTP_400_BAD_REQUEST)
        # if not email:
        #     raise ValueError(_("The Email must be set"))
        # email = self.normalize_email(email)
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        Conta.objects.create(
            cliente=user,
            agencia=numeros(4),
            numero=numeros(6),
            chavePix=str(extra_fields.get('identifier')),
            saldo=saldo(),
            limite=1500,
            ativa=True)

        return user
    
    def create_superuser(self, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(password, **extra_fields)



class Cliente(AbstractBaseUser):
    FISICO = 'F'
    JURIDICO='J'
    TYPES=[
        (FISICO,'Pessoa Física'),
        (JURIDICO,'Pessoa Jurídica'),
    ]
    username = None

    identifier = models.CharField(max_length=14, unique=True)
    inscricao_estadual = models.CharField(max_length=14, null=True)
    inscricao_municipal = models.CharField(max_length=14, null=True)
    rg = models.CharField(max_length=9, unique=True, null=True)
    nome = models.CharField(max_length=100)
    nomeSocial = models.CharField(max_length=100, blank=True)

    # foto = models.ImageField(upload_to='media', blank=True, null=True)
    date_of_birth = models.DateField()

    date_joined = models.DateTimeField(default=timezone.now)

    updated_at =  models.DateTimeField(auto_now=True)

    failed_login_attempts_count = models.IntegerField(default=0)
    blocked_at = models.DateTimeField(null=True)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    
    USERNAME_FIELD = 'identifier'
    # REQUIRED_FIELDS = ['nome','nomeSocial','date_of_birth','foto']
    REQUIRED_FIELDS = ['nome','nomeSocial','date_of_birth',
                       'inscricao_estadual','inscricao_municipal','rg']
    objects = CustomUserManager()

    
    def __str__(self):
        return self.identifier

class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    logradouro = models.CharField(max_length=100)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self) -> str:
        return self.cep
    
class Contato(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    numero = models.CharField(max_length=15, unique=True)
    email = models.CharField(max_length=100, unique=True)
    observacao = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self) -> str:
        return self.email


class Conta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    agencia = models.IntegerField()
    numero = models.IntegerField()
    chavePix = models.CharField(max_length=100, unique=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    ativa = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.cliente.identifier
class Cartoes(models.Model):
    DEBITO = 'd'
    CREDITO = 'c'
    CREBITO = 'b'
    CARTOESLISTA = (
        (DEBITO, "Debito"),
        (CREDITO, "Credito"),
        (CREBITO, "Crebito")
    )
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=CARTOESLISTA, default=CREBITO)
    numero= models.CharField(max_length=20, default="", unique=True)
    bandeira = models.CharField(max_length=1, default='G')

class Movimentacao(models.Model):
    PIX = 'p'
    TRANSFERENCIA = 't'
    CARTAO = 'd'
    TIPOS = (
        (PIX, "Pix"),
        (TRANSFERENCIA, "Transferencia"),
        (CARTAO, "Cartao")
    )
    remetente = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name="remetente")
    remetenteNome = models.CharField(max_length=100)
    destinatario = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name="destinatario")
    destinatarioNome = models.CharField(max_length=100)
    chavePix = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=TIPOS) # PIX TRANFERENCIA PAGAMENTO
    valor = models.DecimalField(max_digits=10, decimal_places=2, default="p")
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=50)
    

class Investimento(models.Model):
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    prazo = models.DateTimeField(auto_now_add=True)    
    saldoInvestido = models.DecimalField(max_digits=10, decimal_places=2)
    local = models.CharField(max_length=50)
    finalizado = models.BooleanField(default=False)

class Emprestimo(models.Model):
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    valor =  models.DecimalField(max_digits=10, decimal_places=2)
    juros = models.DecimalField(max_digits=10, decimal_places=2, default=0.05)
    data = models.DateTimeField(auto_now_add=True)
    valorPagar = models.DecimalField(max_digits=10, decimal_places=2)
    aprovado = models.BooleanField(default=False)
    observacao = models.CharField(max_length=100, blank=True, null=True)


class Parcelas(models.Model):
    emprestimo = models.ForeignKey(Emprestimo, on_delete=models.PROTECT)
    vezes = models.IntegerField(default=1)
    valorParcela = models.DecimalField(max_digits=10, decimal_places=2)
    dataPagamento = models.DateField()
    valorPago = models.DecimalField(max_digits=10, decimal_places=2)