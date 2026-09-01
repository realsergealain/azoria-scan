from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from apps.accounts.models import User
from apps.shop.models import Shop, Order


class ShopNameCooldownAndStatsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="seller@example.com",
            first_name="Aïcha",
            last_name="Vendeuse",
            password="StrongPassword123!"
        )
        self.shop = Shop.objects.create(
            owner=self.user,
            name="Boutique Initiale",
            phone="+2250700000000",
            city="Abidjan"
        )

    def test_shop_name_initial_state(self):
        """Initialement, le nom n'est pas verrouillé."""
        self.assertFalse(self.shop.is_name_locked)
        self.assertEqual(self.shop.name_unlock_days_left, 0)

    def test_shop_name_change_triggers_7_days_cooldown(self):
        """La modification du nom déclenche le verrouillage pour 7 jours."""
        self.shop.name = "Nouveau Nom Boutique"
        self.shop.save()
        self.shop.refresh_from_db()

        self.assertTrue(self.shop.is_name_locked)
        self.assertGreaterEqual(self.shop.name_unlock_days_left, 6)
        self.assertLessEqual(self.shop.name_unlock_days_left, 7)

    def test_shop_name_unlocks_after_7_days(self):
        """Après 7 jours révolus, le nom redevient modifiable."""
        self.shop.name = "Nom Intermédiaire"
        self.shop.save()
        
        # Simuler 8 jours passés
        self.shop.name_last_changed_at = timezone.now() - timedelta(days=8)
        self.shop.save(update_fields=['name_last_changed_at'])
        self.shop.refresh_from_db()

        self.assertFalse(self.shop.is_name_locked)
        self.assertEqual(self.shop.name_unlock_days_left, 0)

    def test_home_view_real_stats_context(self):
        """La vue d'accueil doit exposer les compteurs réels de la plateforme."""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('active_sellers_count', response.context)
        self.assertIn('total_orders_count', response.context)
        self.assertIn('total_products_count', response.context)
        self.assertIn('stats', response.context)
        self.assertGreaterEqual(response.context['active_sellers_count'], 1)
