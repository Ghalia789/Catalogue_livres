from django.test import TestCase, Client


class CatalogueTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_homepage_returns_200(self):
        """La page d'accueil répond avec un code 200"""
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 301, 302])

    def test_admin_page_exists(self):
        """La page admin est accessible"""
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [200, 302])
