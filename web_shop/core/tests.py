from django.test import TestCase, Client
from django.urls import reverse


class IndexViewTest(TestCase):
    """Tests for the index/homepage view"""

    def setUp(self):
        self.client = Client()

    def test_returns_200(self):
        """Should return a 200 status code"""
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)

    def test_sets_csrf_cookie(self):
        """Should set a CSRF cookie (required for JS requests)"""
        response = self.client.get(reverse('core:index'))
        self.assertIn('csrftoken', response.cookies)

    def test_uses_correct_template(self):
        """Should render core/index.html"""
        response = self.client.get(reverse('core:index'))
        self.assertTemplateUsed(response, 'core/index.html')
