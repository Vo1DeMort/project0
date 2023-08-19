from django.db import models
from django.contrib.auth.models import User

class Profile (models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True,upload_to ='images/profile_pics/')
    bio = models.TextField(max_length=150,blank=True)
    link = models.TextField(max_length=300,blank=True)
    joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Post (models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE)
    story = models.TextField(max_length=300)
    pictures = models.ImageField(blank=True,upload_to='images/photos')
    likes = models.ManyToManyField(User,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']

    def no_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return (
            f'{self.owner}'
            f'{self.story}'
            f'{self.created}'
        )

class Comment (models.Model):
    post= models.ForeignKey(Post,on_delete=models.CASCADE)
    writer = models.ForeignKey(Profile,on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'comment by :{self.writer.user.username} on post :{self.post}'





