from django.shortcuts import render,redirect
from blogapp.forms import PostForm,UserProfileForm,RegistrationForm,LoginForm,commentForm
from django.views.generic import View,UpdateView,CreateView,FormView,DetailView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from blogapp.decorators import login_required
from django.urls import reverse
from blogapp.models import UserProfile,Post,Comments,Category


decs=[login_required,never_cache]
class signUpView(CreateView):
    template_name="register.html"
    form_class=RegistrationForm

    def get_success_url(self):
        return reverse("log-in")

@method_decorator(decs,name="dispatch")
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
        
@method_decorator(decs,name="dispatch")
class HomeView(View):
    
        def get(self,request,*args,**kwargs):
            posts=Post.objects.all()
        
            post_comments={}       
            for post in posts:
            
                post_comments[post]=Comments.objects.filter(post=post)
                
                all_comments = []

# Iterate over the values of the dictionary
                for comments_queryset in post_comments.values():
    # Iterate over each comment queryset
                    for comment in comments_queryset:
                        all_comments.append(comment)
        
            return render(request,"index.html",{"post_comments":post_comments})
        
        # qs=Post.objects.all()
        # return render(request,"index.html",{"data":qs})
        
@method_decorator(decs,name="dispatch")
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
                return redirect("home") 
            # else:
            #     return redirect("log-in")  
        messages.error(request,"invalid credentials")  
        return render(request,"login.html",{"form":form})  
@method_decorator(decs,name="dispatch")    
class profileDetailView(DetailView):
    template_name="profile_detail.html"
    model=UserProfile
    context_object_name="data"

@method_decorator(decs,name="dispatch")
class profilelistView(View):
    def get(self,request,*args,**kwargs) :
        qs=UserProfile.objects.all().exclude(user=request.user)
        return render(request,"profile_list.html",{"data":qs})
@method_decorator(decs,name="dispatch")
class postdeleteView(View):
    def get(self,request,pk,*args,**kwargs):
        post_id=kwargs.get("pk")
        Post.objects.get(post_id=pk).delete()
        return redirect("home")
@method_decorator(decs,name="dispatch")    
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
    
@method_decorator(decs,name="dispatch")
class CommentView(CreateView) :
    template_name="index.html"   
    form_class=commentForm

    def get_success_url(self):
        return reverse("home")
    

    def form_valid(self,form):
        post_id=self.kwargs.get("pk")
        post_object=Post.objects.get(post_id=post_id)
        form.instance.user=self.request.user
        form.instance.post=post_object
        return super().form_valid(form)
    
@method_decorator(decs,name="dispatch")
class categorylistView(View):
    def get(self,request,*args,**kwargs):
        category=Category.objects.all()
        
        return render(request,"index.html",{"cat":category})    
@method_decorator(decs,name="dispatch")
class categoryPostView(View):
    def get(self,request,category_title,*args,**kwargs):
        category=Category.objects.get(title=category_title)
        posts=Post.objects.filter(cat=category_title)
        return render(request,"category_post.html",{"category":category,"posts":posts})
@method_decorator(decs,name="dispatch")    
class SignOutView(View):
    def get(self,request,*args,**kwargs) :
        logout(request) 
        return redirect("log-in")  