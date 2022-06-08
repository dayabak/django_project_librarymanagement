from django import forms
from . models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BookAddForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ('name','author','isbn','publisher')
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'author': forms.TextInput(attrs={'class':'form-control'}),
			'isbn': forms.TextInput(attrs={'class':'form-control'}),
			'publisher': forms.TextInput(attrs={'class':'form-control'}),
		}
		labels = {
			'name': 'Book Name',
			'author': 'Author Name',
			'isbn': 'ISBN',
			'publisher': 'Publisher'
		}


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
		
		widgets = {
			'username': forms.TextInput(attrs={'class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
			'first_name': forms.TextInput(attrs={'class':'form-control'}),
			'last_name': forms.TextInput(attrs={'class':'form-control'}),
		}
		labels = {
			'username': 'Username',
			'email': 'Email',
			'first_name': 'First Name',
			'last_name': 'Last Name',
			'password1': 'Password',
			'password2': 'Re-enter Password'
		}

	def __init__(self, *args, **kwargs):
			super(CreateUserForm, self).__init__(*args, **kwargs)
			self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
			self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
	
	def clean_email(self):
		email = self.cleaned_data.get('email')
		user_count = User.objects.filter(email=email).count()
		if user_count > 0:
			raise forms.ValidationError("Email already exists!")
		return email
	
	def save(self, commit=True):
		user = super(CreateUserForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user