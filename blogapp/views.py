from django.shortcuts import render,redirect
from blogapp.forms import PostForm,UserProfileForm,RegistrationForm,LoginForm,commentForm
from django.views.generic import View,UpdateView,CreateView,FormView,DetailView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from blogapp.models import UserProfile,Post,Comments

class signUpView(CreateView):
    template_name="register.html"
    form_class=RegistrationForm

    def get_success_url(self):
        return reverse("signin")

class postCreateView(View):
    def get(self,request,*args,**kwargs):
        form=PostForm()
        return render(request,"create.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=PostForm(request.POST,files=request.FILES)
        if form.is_valid():
            print("valid")
            form.save()
            print("success")
            messages.success(request,"post created")
            return redirect("home")
        else:
            messages.error(request,"failed to create the post")
            return render(request,"create.html",{"form":form})
        

class HomeView(View):
    def get(self,request,*args,**kwargs):
        
        qs=Post.objects.all()
        return render(request,"index.html",{"data":qs})
        

class profileUpdateView(UpdateView):
    template_name="profile_add.html" 
    form_class=UserProfileForm    
    model=UserProfile 

    def get_success_url(self):
        return reverse("home")
    

class SignInView(FormView):
    template_name="login.html"    
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
            else:
                return redirect("home")  
        messages.error(request,"invalid credentials")  
        return render(request,"login.html",{"form":form})  
    
class profileDetailView(DetailView):
    template_name="profile_detail.html"
    model=UserProfile
    context_object_name="data"


class profilelistView(View):
    def get(self,request,*args,**kwargs) :
        qs=UserProfile.objects.all().exclude(user=request.user)
        return render(request,"profile_list.html",{"data":qs})

class postdeleteView(View):
    def get(self,request,pk,*args,**kwargs):
        post_id=kwargs.get("pk")
        Post.objects.get(post_id=pk).delete()
        return redirect("home")
    
class CommentView(CreateView):
    template_name="index.html"   
    form_class=commentForm 
    

    def get_success_url(self):
        return reverse("home")
    
   
        
    def form_valid(self, form):
        id=self.kwargs.get("pk")
        post_object=Post.objects.get(id=id)
        form.instance.user=self.request.user#passing instance and user in then form
        form.instance.post=post_object
        return super().form_valid(form)