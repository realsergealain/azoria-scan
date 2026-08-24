from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        """Vérifie que la page d'accueil retourne un code 200."""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        """Vérifie que le bon template est utilisé."""
        response = self.client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_home_page_content(self):
        """Vérifie la présence des éléments clés de la marque Azoria."""
        response = self.client.get(reverse('core:home'))
        self.assertContains(response, 'Azoria')
        self.assertContains(response, 'Social Commerce')
        self.assertContains(response, 'TikTok')
        self.assertContains(response, 'WhatsApp')
        self.assertContains(response, 'Paiement à la livraison')
