from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from datetime import timedelta, datetime
from django.utils import timezone

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, identifier=None, password=None, **kwargs):
        print('passou aki')
        User = get_user_model()
        try:
            user = User.objects.get(identifier=identifier)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            # A senha está correta. Reinicie a contagem de tentativas.
            user.failed_login_attempts_count = 0
            if not user.is_active and user.blocked_at:
                reactivation_period = timedelta(minutes=3)  # Defina o período de reativação (7 dias neste exemplo)
                if timezone.now() - user.blocked_at > reactivation_period:
                    user.is_active = True
                    user.blocked_at = None  # Redefina o campo de bloqueio
                
            user.save()
            return user
        else:
            # A senha está incorreta. Incremente a contagem de tentativas.
            user.failed_login_attempts_count += 1
            user.save()
            
            # Verifique se a conta deve ser bloqueada.
            if user.failed_login_attempts_count >= 3:
                user.is_active = False
                user.blocked_at = timezone.now()
                user.save()
                # raise AccountBlocked("Sua conta foi bloqueada. Entre em contato com o suporte.")
            
            
            return None
        
    # def user_can_authenticate(self, user):
    #     # Verifique se a conta está bloqueada e se passou tempo suficiente para reativação
    #     print('auth passou aki')
        
        
    #     return super().user_can_authenticate(user)