from django.urls import path
from . import views

urlpatterns = [
	# Auth Urls ---------------------->
	path('register/', views.registerUser, name='register'),
	path('login/', views.loginUser, name='login'),
	path('logout/', views.logoutUser, name='logout'),

	# Default View (Students) --------->
	path('', views.showAll, name='books_list'),

	# Admin Menu ---------------------->
	path('library/managebooks/', views.manageBooks, name='manageBooks'),
	path('library/addbook/', views.addBook, name='addBook'),
	path('library/bookupdate/<int:pk>/', views.updateBook, name='updateBook'),
	path('library/bookdelete/<int:pk>/', views.deleteBook, name='deleteBook'),
]