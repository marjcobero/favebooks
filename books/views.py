from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

def index(request):
    request.session.flush()
    return render(request, 'register.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return  redirect('/')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'], 
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw,
        )
        request.session['user_id'] = new_user.id
        return redirect('/books')
    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return  redirect('/')
    if request.method == 'POST':
        the_user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), the_user.password.encode()):
            print(request.method)
            request.session['user_id'] = the_user.id
            request.session['greeting'] = the_user.first_name
            return redirect('/books')
        messages.error(request, "Email or Password incorrect")
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def show_all(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'all_books': Book.objects.all(),
            'the_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'showall.html', context)

def create_book(request):
    errors = Book.objects.book_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            creator = user
        )
        user.favorited_books.add(book)
        return redirect(f'/books/{book.id}')

def show_one(request, user_id):
    context = {
        'book': Book.objects.get(id=user_id),
        'the_user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, "showone.html", context)

def update(request, user_id):
    book = Book.objects.get(id=user_id)
    book.description = request.POST['description']
    book.save()
    return redirect(f'/books/{user_id}')

def delete(request, user_id):
    book = Book.objects.get(id=user_id)
    book.delete()
    return redirect('/books')

def favorite(request, user_id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=user_id)
    user.favorited_books.add(book)
    return redirect(f'/books/{user_id}')

def unfavorite(request, user_id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=user_id)
    user.favorited_books.remove(book)
    return redirect(f'/books/{user_id}')