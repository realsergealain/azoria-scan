from django.test import TestCase
from django.urls import reverse
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


class AuthViewsTests(TestCase):
    def setUp(self):
        self.email = 'mariam@boutique.ci'
        self.password = 'SuperSecret123!'
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name='Mariam',
            last_name='Diallo',
            phone='+2250700000000',
        )

    def test_login_page_renders_correctly(self):
        """Vérifie que la page de login renvoie un code 200 et les bons éléments."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, 'Connexion')
        self.assertContains(response, 'Continuer avec Google')

    def test_login_successful(self):
        """Vérifie la connexion réussie avec des identifiants valides."""
        response = self.client.post(reverse('accounts:login'), {
            'email': self.email,
            'password': self.password,
            'remember_me': 'on',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_invalid_credentials(self):
        """Vérifie le message d'erreur lors d'une mauvaise tentative de connexion."""
        response = self.client.post(reverse('accounts:login'), {
            'email': self.email,
            'password': 'WrongPassword999!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], None, "Identifiants incorrects. Veuillez vérifier votre adresse email et mot de passe.")

    def test_register_page_renders_correctly(self):
        """Vérifie que la page d'inscription renvoie un code 200."""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertContains(response, 'Créer un compte')
        self.assertContains(response, 'Continuer avec Google')

    def test_register_successful(self):
        """Vérifie l'inscription complète et la redirection."""
        new_email = 'koffi.nouveau@boutique.ci'
        response = self.client.post(reverse('accounts:register'), {
            'full_name': 'Koffi Serge Alain',
            'email': new_email,
            'phone': '0505050505',
            'password': 'NouveauMotDePasse123!',
            'password_confirm': 'NouveauMotDePasse123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email=new_email).exists())
        created_user = User.objects.get(email=new_email)
        self.assertEqual(created_user.first_name, 'Koffi')
        self.assertEqual(created_user.last_name, 'Serge Alain')

    def test_logout(self):
        """Vérifie la déconnexion."""
        self.client.login(username=self.email, password=self.password)
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)
