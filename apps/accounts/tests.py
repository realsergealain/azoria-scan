from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Vérifie la création d'un utilisateur régulier avec email."""
        email = 'vendeur@azoria.ci'
        password = 'AzoriaPassword123!'
        user = User.objects.create_user(email=email, password=password, first_name='Aïcha', last_name='Kouamé')
        
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.full_name, 'Aïcha Kouamé')

    def test_create_superuser(self):
        """Vérifie la création d'un superutilisateur."""
        admin_user = User.objects.create_superuser(
            email='admin@azoria.ci',
            password='AdminPassword123!'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_create_user_without_email_raises_error(self):
        """Vérifie qu'une erreur est levée sans email."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='testpassword')
