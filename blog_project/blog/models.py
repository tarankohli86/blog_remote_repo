from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class CustomManager(models.Manager):
     def get_queryset(self):
          return super().get_queryset().filter(status="published")
     

from taggit.managers import TaggableManager

class POST(models.Model):
     STATUS_CHOICES=(('draft','Draft'),('published','Published'))
     title=models.CharField(max_length=256)
     slug=models.SlugField(max_length=264,unique_for_date="publish")
     author=models.ForeignKey(User,related_name="blog_post",on_delete=models.CASCADE)
     body=models.TextField()
     publish=models.DateTimeField(default=timezone.now)
     # on what did this is post got created
     # whenever this post object got created that time will be considered
     created=models.DateTimeField(auto_now_add=True)
     
     # this will take at what time the save method is called
     updated=models.DateTimeField(auto_now=True)
     status=models.CharField(max_length=10,choices=STATUS_CHOICES,default="draft")
     objects=CustomManager()
     tags=TaggableManager()
     #post will be in the most recent 
     class Meta:
        ordering=('-publish',)
     
     # if anywhere we display our post then the title will` be displayed
     def __str__(self):
          return self.title
      
     def get_absolute_url(self):
          return reverse("post_detail",args=[self.publish.year,self.publish.strftime("%m"),self.publish.strftime("%d"),self.slug] )
     

class Comment(models.Model):
     post=models.ForeignKey(POST,related_name="comments",on_delete=models.CASCADE)
     name=models.CharField(max_length=30)
     email=models.EmailField()
     body=models.TextField()
     created=models.DateTimeField(auto_now_add=True)
     update=models.DateTimeField(auto_now=True)
     active=models.BooleanField(default=True)

     class Meta:
          # new first old last
          ordering=('created',)

     def __str__(self):
          return 'Commented by {} on {}'.format(self.name,self.post)