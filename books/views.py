from django.shortcuts import render
from .models import Book


def books_view(request, date=None):
    template = 'books/books_list.html'
    books = Book.objects.order_by('pub_date')

    if date is None:
        context = {'books': books}
    else:
        books = Book.objects.filter(pub_date=date).all()

        pred_date = Book.objects.filter(pub_date__lt=date).values('pub_date').first()
        next_date = Book.objects.filter(pub_date__gt=date).values('pub_date').last()

        context = {'books': books,
                   'next_date': pred_date['pub_date'].strftime('%Y-%m-%d') if pred_date is not None else None,
                   'pred_date': next_date['pub_date'].strftime('%Y-%m-%d') if next_date is not None else None,
                   }

    return render(request, template, context)
