from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone
from datetime import timedelta
from order.models import Order
from book.models import Book
from authentication.models import CustomUser

LOAN_PERIOD = timedelta(weeks=2)

def create_an_order(request):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        user_id = request.POST.get('user')

        book = Book.get_by_id(book_id)
        user = CustomUser.get_by_id(user_id)

        if book is None or user is None:
            raise Http404("Book or user not found")

        plated_end_at = timezone.now() + LOAN_PERIOD
        order = Order.create(user=user, book=book, plated_end_at=plated_end_at)

        if order is None:
            return render(request, 'order/create_an_order.html', {'error': 'No copies available.'})

        return redirect('user_orders', user_id=user.id)

    return render(request, 'order/create_an_order.html')

def close_an_order(request, order_id):
    order = Order.get_by_id(order_id)
    if order is None:
        raise Http404("Not found")
    if request.method == 'POST':
        order.update(end_at=timezone.now())
        return redirect('list_of_orders')
    return render(request, 'order/close_an_order.html', {'order': order})

def user_orders(request, user_id):
    orders = Order.objects.filter(user_id=user_id)
    return render(request, 'order/user_orders.html', {'orders': orders})
 
def list_of_orders(request):
    orders = Order.objects.all()
    return render(request, 'order/list_of_orders.html', {'orders': orders})