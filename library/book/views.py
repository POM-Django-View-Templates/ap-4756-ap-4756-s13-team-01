# Create your views here.
from django.shortcuts import render, redirect
from django.http import Http404
from book.models import Book
from order.models import Order

def book_detail(request, book_id):
    book = Book.get_by_id(book_id)
    if book is None:
        raise Http404("Not found")
    return render(request, 'book/book_detail.html', {'book': book})

def create_a_book(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        count = request.POST.get('count')
        book = Book.create(name, description, count)
        return redirect('book_detail', book_id=book.id)
    return render(request, 'book/create_a_book.html')

def list_of_books(request):
    books = Book.objects.all()
    name = request.GET.get('name')
    author = request.GET.get('author')

    if name:
        books = books.filter(name__icontains=name)
    if author:
        books = books.filter(author__icontains=author)

    return render(request, 'book/list_of_books.html', {'books': books})

def ordered_books_by_user(request, user_id):
    orders = Order.objects.filter(user_id=user_id)
    return render(request, 'book/ordered_books_by_user.html', {'orders': orders})