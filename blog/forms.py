from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text','tags','category','header_img')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'multiple data-style':'bg-white px-4 py-3 shadow-sm','class': 'selectpicker w-100'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            
        }



