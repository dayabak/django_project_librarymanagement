from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from . models import Book
from .forms import BookAddForm, CreateUserForm
from . serializers import BookSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from rest_framework.response import Response
from rest_framework.decorators import api_view


def registerUser(request):
	if request.user.is_authenticated:
		return redirect('manageBooks')
	else:
		form = CreateUserForm()

		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account created successfuly for '+user)
				return redirect('login')

		context = {'form':form}
		return render(request, 'library/register.html', context)


def loginUser(request):
	if request.user.is_authenticated:
		return redirect('manageBooks')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('manageBooks')
			else:
				messages.info(request, 'Username or Password incorrect!!')

		context = {}
		return render(request, 'library/login.html')


def logoutUser(request):
	logout(request)
	return redirect('login')


@api_view(['GET'])
def showAll(request):
	books = Book.objects.all()
	serializer = BookSerializer(books, many=True)
	context = {
		'book_list': serializer.data
	}
	return render(request, 'library/books_list.html', context)


@login_required(login_url='login')
@api_view(['GET'])
def manageBooks(request):
	books = Book.objects.all()
	serializer = BookSerializer(books, many=True)
	context = {
		'book_list': serializer.data
	}
	return render(request, 'library/books_actions.html', context)


@login_required(login_url='login')
@api_view(['GET', 'POST'])
def addBook(request):
	if request.method == "GET":
		form = BookAddForm()
		return render(request, "library/book_update.html", {'form':form})
	elif request.method == "POST":
		form = BookAddForm(request.POST)
		if form.is_valid():
			serializer = BookSerializer(data=form.data)
			if serializer.is_valid():
				serializer.save()
		return redirect('manageBooks')


@login_required(login_url='login')
@api_view(['GET', 'POST'])
def updateBook(request, pk):
	if request.method == "GET":
		book = Book.objects.get(id=pk)
		form = BookAddForm(instance=book)
		return render(request, "library/book_update.html", {'form':form})
	elif request.method == "POST":
		book = Book.objects.get(id=pk)
		form = BookAddForm(request.POST, instance=book)
		if form.is_valid():
			serializer = BookSerializer(instance=book, data=form.data)
			if serializer.is_valid():
				serializer.save()
		return redirect('manageBooks')

@login_required(login_url='login')
@api_view(['POST'])
def deleteBook(request, pk):
	book = Book.objects.get(id=pk)
	book.delete()
	return redirect('manageBooks')