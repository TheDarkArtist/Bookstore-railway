from django.test import SimpleTestCase
from django.urls  import reverse, resolve

from .views import HomePageView, AboutPageView


class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_page_url_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_page_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_home_page_contains_correct_html(self):
        self.assertContains(self.response, 'Home page')

    def test_home_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'This should not be on the page')

    def test_home_page_url_resolves_home_page_url(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AboutPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('about')
        self.response = self.client.get(url)

    def test_about_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_about_page_template_exists(self):
        self.assertTemplateUsed(self.response, 'about.html')

    def test_about_page_contans_correct_html(self):
        self.assertContains(self.response, 'about page')

    def test_about_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'This sould not be the html')

    def test_aboutpage_url_resolves_to_aboutpageview(self):
        view = resolve('/about/')
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)