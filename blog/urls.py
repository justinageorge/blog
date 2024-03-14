"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from blogapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/create/',views.postCreateView.as_view(),name="createpost"),
    path("home/",views.HomeView.as_view(),name="home"),
    path("profileadd/<int:pk>/",views.profileUpdateView.as_view(),name="pupdate"),
    path("register",views.signUpView.as_view(),name="signin"),
    path("login/",views.SignInView.as_view(),name="log-in"),
    path("profiles/<int:pk>/",views.profileDetailView.as_view(),name="update"),
    path("profiles/all",views.profilelistView.as_view(),name="profilelist"),
    path("postdelete/<int:pk>/",views.postdeleteView.as_view(),name="delete"),
    path("postcomments/",views.CommentView.as_view(),name="comments")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
