from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adaptateur personnalisé pour gérer la création et liaison automatique
    des comptes sociaux (Google, etc.) avec les utilisateurs Azoria.
    """

    def populate_user(self, request, sociallogin, data):
        """
        Pré-remplit les champs de l'utilisateur (nom, prénom) à partir des données fournies par le provider.
        """
        user = super().populate_user(request, sociallogin, data)
        extra_data = sociallogin.account.extra_data

        if not user.first_name:
            user.first_name = extra_data.get('given_name') or ''
        if not user.last_name:
            user.last_name = extra_data.get('family_name') or ''

        return user
