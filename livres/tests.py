from django.test import TestCase


class LivreViewsTest(TestCase):

    def test_home_page(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_book_list(self):
        response = self.client.get('/books')
        self.assertEqual(response.status_code, 200)

    def test_redirect_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 301)
