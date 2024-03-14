from django import forms
from blogapp.models import Post,UserProfile,Comments,Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):

    
    class Meta:
        model=Post
        fields=['title', 'content', 'url', 'cat', 'image']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile 
        exclude=['user','following','block']   
        widgets={
            "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }   

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"] 

class LoginForm(forms.Form) :
    username=forms.CharField()
    password=forms.CharField()

class commentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=['text']    
