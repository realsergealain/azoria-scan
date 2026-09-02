import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modèle utilisateur personnalisé pour Azoria.
    Utilise l'email comme identifiant principal et un UUID public.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('adresse email'), unique=True, max_length=255)
    phone = models.CharField(_('numéro de téléphone'), max_length=20, blank=True, null=True)
    first_name = models.CharField(_('prénom'), max_length=150, blank=True)
    last_name = models.CharField(_('nom'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('statut équipe'),
        default=False,
        help_text=_('Désigne si l\'utilisateur peut se connecter au site d\'administration.'),
    )
    is_active = models.BooleanField(
        _('actif'),
        default=True,
        help_text=_('Désigne si ce compte doit être traité comme actif.'),
    )
    date_joined = models.DateTimeField(_('date d\'inscription'), default=timezone.now)
    updated_at = models.DateTimeField(_('dernière mise à jour'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')
        ordering = ['-date_joined']

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.email})"
        return self.email

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or self.email.split('@')[0]


class PushSubscription(models.Model):
    """
    Abonnement Web Push du navigateur pour recevoir des alertes hors-ligne.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_subscriptions')
    endpoint = models.TextField(unique=True, verbose_name=_('Endpoint Push'))
    p256dh = models.CharField(max_length=255, verbose_name=_('Clé publique p256dh'))
    auth = models.CharField(max_length=255, verbose_name=_('Clé auth'))
    user_agent = models.CharField(max_length=500, blank=True, null=True, verbose_name=_('User Agent'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date de création'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Dernière mise à jour'))

    class Meta:
        verbose_name = _('Abonnement Web Push')
        verbose_name_plural = _('Abonnements Web Push')
        ordering = ['-created_at']

    def __str__(self):
        return f"Push {self.user.email} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"
