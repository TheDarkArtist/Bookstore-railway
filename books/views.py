from django.db.models import Q
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic import ListView, DetailView
from .models import *

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = "books/book_list.html"
    login_url = 'account_login' 

class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_details.html'
    login_url = 'account_login'
    permission_required = "books.special_status"
    queryset = Book.objects.all().prefetch_related('reviews__author')

class SearchResultListView(ListView):
    model = Book
    context_object_name='book_list'
    template_name = "books/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
         Q(title__icontains=query) | Q(title__icontains=query) 
        )
    