from django.test import TestCase
from django.contrib.auth.models import Permission
from django.urls import reverse

from .models import *


class BookTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'reviewuser@email.com',
            password = 'testpass123',
        )
        cls.special_permission = Permission.objects.get(
            codename='special_status'
        )
        cls.book = Book.objects.create(
            title='The Test Title',
            author='testauthor',
            price='299.00'
        )
        cls.review  = Review.objects.create(
            book=cls.book,
            author=cls.user,
            review='Test review'
        )
    

    
    def test_book_listing(self):
        self.assertEqual(f"{self.book.title}", "The Test Title")
        self.assertEqual(f"{self.book.author}", "testauthor")
        self.assertEqual(f"{self.book.price}", '299.00')

    
    def test_book_list_view_for_loged_im_user(self):
        self.client.login(
            email="reviewuser@email.com",
            password="testpass123"
        )
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The Test Title')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_list_view_for_loged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "%s?next=/books/" % (reverse('account_login'))
        )
        response = self.client.get(
            "%s?next=/books/" % (reverse('account_login'))
        )
        self.assertContains(response, 'Log In')
    
    def test_book_detail_view_with_permission(self):
        self.client.login(
            email="reviewuser@email.com",
            password="testpass123"
        )
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('books/352435')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "The Test Title")
        self.assertContains(response, 'Test review')
        self.assertTemplateUsed(response, 'books/book_details.html')

