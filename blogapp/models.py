from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile",null=True)
    address=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    profile_pic=models.ImageField(upload_to="profile_pics",null=True,blank=True)
    dob=models.DateField(null=True)
    bio=models.CharField(max_length=200,null=True)
    following=models.ManyToManyField("self",related_name="followed_by",symmetrical=False,null=True)
    block=models.ManyToManyField("self",related_name="blocked",symmetrical=False,null=True)
    def __str__(self):
        return self.user.username
class Category(models.Model):
    cat_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=200)
    description=models.TextField()
    url=models.CharField(max_length=100)
    image=models.ImageField(upload_to='category/')
    add_date=models.DateTimeField(auto_now_add=True,null=True)

 

CATEGORIES = (
    ('technology', 'Technology'),
    ('science', 'Science'),
    ('education', 'Education'),
    ('art', 'Art'),
    ('food', 'Food'),
    ('fashion', 'Fashion'),
    ('others', 'Others'),
)

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    url = models.CharField(max_length=100)
    cat = models.CharField(max_length=100, choices=CATEGORIES)
    image = models.ImageField(upload_to='posts/')
class Comments(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="postcomment")    
    user=models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
def create_profile(sender,created,instance,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_profile,sender=User)        